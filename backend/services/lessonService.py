from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.models.lessonModel import Lesson
from backend.schemas.lessonSchema import LessonCreate, LessonResponse
from datetime import datetime, timedelta
from dateutil.parser import parse
from backend.services.Google_apiService import calculate_departure_time, calculate_travel_time, is_time_slot_available
import pytz

EXTRA_TIME = 30

def create_lesson(db: Session, lesson_data: LessonCreate, user_id: int):
    """Creates a new lesson in the database."""
    try:
        new_lesson = Lesson(
            user_id=user_id,
            date=lesson_data.date,
            start_time=lesson_data.start_time,
            end_time=lesson_data.end_time,
            location=lesson_data.location,
            adress=lesson_data.adress,  # Make sure it's not causing issues
            status=lesson_data.status,
            lesson_name=lesson_data.lesson_name,
            class_number=lesson_data.class_number,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(new_lesson)
        db.commit()
        db.refresh(new_lesson)

        return LessonResponse(
            lesson_id=new_lesson.lesson_id,
            user_id=new_lesson.user_id,
            date=new_lesson.date,  
            start_time=new_lesson.start_time,
            end_time=new_lesson.end_time,
            location=new_lesson.location,
            adress=new_lesson.adress,
            status=new_lesson.status,
            lesson_name=new_lesson.lesson_name,
            class_number=new_lesson.class_number,
            created_at=new_lesson.created_at,
            updated_at=new_lesson.updated_at
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to create lesson: {str(e)}"}
        )


def get_possible_time_slots(lesson_data: LessonCreate, events):
    """ Identify available time slots for a new lesson by analyzing existing calendar events and travel time constraints. """
    print("Finding possible time slots...")
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
                    lesson_data.adress, event_location, event_start_time
                )

                lesson_end_before_event = parse(lesson_departure_time) - timedelta(minutes=EXTRA_TIME)
                lesson_start_before_event = lesson_end_before_event - timedelta(minutes=lesson_data.duration)

                if is_time_slot_available(events, lesson_start_before_event, lesson_end_before_event):
                    possible_slots.append((lesson_start_before_event, lesson_end_before_event))

            except Exception as e:
                raise Exception(f"Error: {str(e)}")

            try:
                # ---------------- AFTER EVENT ----------------
                travel_duration_minutes = calculate_travel_time(
                    event_location, lesson_data.adress, event_end_time
                )

                lesson_start_after_event = event_end_time + timedelta(minutes=travel_duration_minutes + EXTRA_TIME)
                lesson_end_after_event = lesson_start_after_event + timedelta(minutes=lesson_data.duration)

                if is_time_slot_available(events, lesson_start_after_event, lesson_end_after_event):
                    possible_slots.append((lesson_start_after_event, lesson_end_after_event))

            except Exception as e:
                print(f"Error: {str(e)}")
                continue  # Skip this and move to the next event

    return possible_slots
