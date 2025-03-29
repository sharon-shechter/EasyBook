from sqlalchemy.orm import Session 
from datetime import datetime, timedelta , time
from dateutil.parser import parse
from app.services.Google_apiService import calculate_departure_time, calculate_travel_time, is_time_slot_available, add_lesson_to_calendar, delete_event_from_calendar
from app.repositories.lessonRepositorie import create_lesson , delete_lesson_from_db , get_lessons_by_lesson_id
from fastapi import HTTPException
from googleapiclient.errors import HttpError

import pytz

EXTRA_TIME = 30

def create_lesson_service(db: Session, lesson_data, user_id: int, status: int, google_service):
    """Handles business logic for lesson creation."""
    google_event_id = add_lesson_to_calendar(google_service, db ,  lesson_data, user_id)
    new_lesson  = create_lesson(db, lesson_data, user_id, google_event_id, status)
    return new_lesson



def delete_lesson_service(lesson_id: int, user_id: int, google_service, db: Session):
    try:
        lesson = get_lessons_by_lesson_id(db, lesson_id)
        event_id = lesson.google_event_id

        if not event_id:
            raise HTTPException(status_code=404, detail="Lesson does not have a Google Calendar event")

        delete_event_from_calendar(google_service, event_id)
        delete_lesson_from_db(db, lesson_id)

    except HTTPException as http_exc:
        raise http_exc  # Re-raise FastAPI exceptions directly

    except HttpError as http_error:
        if http_error.status_code == 410:
            raise HTTPException(status_code=404, detail="Google Calendar event already deleted.")
        raise HTTPException(status_code=500, detail=f"Google Calendar error: {http_error}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while deleting lesson: {e}")

    return True
    

def round_to_nearest_five(dt):
    """Round datetime to the nearest 5-minute mark."""
    minute = (dt.minute // 5) * 5
    rounded_dt = dt.replace(minute=minute, second=0, microsecond=0)
    if dt.minute % 5 >= 3:
        rounded_dt += timedelta(minutes=5)

    return rounded_dt


def generate_full_day_slots(lesson_date, lesson_duration):
    """Generate time slots from 8:00 AM to 9:00 PM based on lesson duration."""
    try : 
        slots = []
        current_time = datetime.combine(lesson_date, time(8, 0)) 
        end_of_day = datetime.combine(lesson_date, time(21, 0))  

        while current_time < end_of_day:
            end_time = current_time + timedelta(minutes=lesson_duration)

            if end_time <= end_of_day:
                slots.append((current_time, end_time))

            current_time = end_time

        return slots
    except Exception as e:
        raise Exception(f"Error generating time slots for a fre day: {str(e)}")


def get_possible_time_slots( lesson_adress, lesson_duration, events):
    """ Identify available time slots for a new lesson by analyzing existing calendar events and travel time constraints. """
    possible_slots = []
    tz = pytz.timezone("Asia/Jerusalem")

    for event in events:
        try:
            event_start_iso = event["start"].get("dateTime")
            event_end_iso = event["end"].get("dateTime")
            event_location = event.get("location")

            # Convert the string to datetime object
            event_start_time = datetime.fromisoformat(event_start_iso).astimezone(tz)
            event_end_time = datetime.fromisoformat(event_end_iso).astimezone(tz)

        except Exception as e:
            raise Exception(f"Error parsing event data: {str(e)}")
        
        if event_location:
            try:
                # ---------------- BEFORE EVENT ----------------
                lesson_departure_time = calculate_departure_time(
                    lesson_adress, event_location, event_start_time
                )

                lesson_end_before_event = round_to_nearest_five(parse(lesson_departure_time) - timedelta(minutes=EXTRA_TIME))
                lesson_start_before_event = round_to_nearest_five (lesson_end_before_event - timedelta(minutes=lesson_duration))

                if is_time_slot_available(events, lesson_start_before_event, lesson_end_before_event):
                    possible_slots.append((lesson_start_before_event, lesson_end_before_event))

            except Exception as e:
                raise Exception(f"Error: {str(e)}")

            try:
                # ---------------- AFTER EVENT ----------------
                travel_duration_minutes = calculate_travel_time(
                    event_location, lesson_adress, event_end_time
                )

                lesson_start_after_event = round_to_nearest_five (event_end_time + timedelta(minutes=travel_duration_minutes + EXTRA_TIME))
                lesson_end_after_event = round_to_nearest_five(lesson_start_after_event + timedelta(minutes=lesson_duration))

                if is_time_slot_available(events, lesson_start_after_event, lesson_end_after_event):
                    possible_slots.append((lesson_start_after_event, lesson_end_after_event))

            except Exception as e:
                raise Exception(f"Error: {str(e)}")

    return possible_slots


