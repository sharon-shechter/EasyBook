from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy.orm import Session
from datetime import time
from fastapi import HTTPException
import googlemaps
import pytz
from backend.schemas.lessonSchema import LessonCreate
from backend.services.userService import get_user_full_name
from config import token, credentials, Google_API_KEY




SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticate_google_calendar():
    """Authenticate using credentials from config.py."""
    creds = None

    try:
        if token:
            creds = Credentials.from_authorized_user_info(token, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(credentials, SCOPES)
                creds = flow.run_local_server(port=0)

        return build("calendar", "v3", credentials=creds)

    except Exception as e:
        raise Exception(f"Google API authentication failed: {str(e)}")

def get_events_of_date(service, date):
    """
    Get all events for a given date from the authenticated Google Calendar.
    """
    try:
        tz = pytz.timezone("Asia/Jerusalem") 

        start_of_day = tz.localize(datetime.combine(date, datetime.min.time())).isoformat()
        end_of_day = tz.localize(datetime.combine(date, datetime.max.time())).isoformat()

        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        events = events_result.get("items", [])
        return events

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching events: {str(e)}")
    
def is_reasonable_time_slot(start_time, end_time):
    """Make sure the time slot is reasonable"""
    try:
        earliest_time = time(8, 0)  
        latest_time = time(21, 0)  

        # Extract time portion from datetime
        start_time_hour = start_time.time()
        end_time_hours = end_time.time()

        if start_time_hour < earliest_time or start_time_hour > latest_time:
            return False
        if end_time_hours > latest_time:
            return False
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking time slot reasonable: {str(e)}")

def is_time_slot_available(events, start_time, end_time):
    """
    Check if a given time slot is available.
    """
    if not is_reasonable_time_slot(start_time, end_time):
        return False
    if not events:
        return True  

    try:
        tz = pytz.timezone("Asia/Jerusalem")

        if start_time.tzinfo is None:
            start_time = tz.localize(start_time)
        if end_time.tzinfo is None:
            end_time = tz.localize(end_time)

        for event in events:
            event_start_str = event["start"].get("dateTime")
            event_end_str = event["end"].get("dateTime")

            if event_start_str and event_end_str:
                event_start = datetime.fromisoformat(event_start_str).astimezone(tz)
                event_end = datetime.fromisoformat(event_end_str).astimezone(tz)

                if not (end_time <= event_start or start_time >= event_end):
                    return False  
        return True  

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking time slot availability: {str(e)}")
    

def add_lesson_to_calendar(service, db :Session ,lesson: LessonCreate, user_id: int):
    """
    Adds a lesson to Google Calendar with the user's name in the summary.
    """
    try:
        tz = pytz.timezone("Asia/Jerusalem")
        start_datetime = tz.localize(datetime.combine(lesson.date, lesson.start_time))
        end_datetime = tz.localize(datetime.combine(lesson.date, lesson.end_time))

        # Fetch the user name from the database
        user_name = get_user_full_name(db, user_id)
        event = {
            "summary": f"{lesson.lesson_name} with {user_name}", 
            "location": lesson.lesson_adress,
            "description": f"Lesson Type: {lesson.lesson_type}\nClass Number: {lesson.class_number}",
            "colorId": "11",
            "start": {
                "dateTime": start_datetime.isoformat(),
                "timeZone": "Asia/Jerusalem",
            },
            "end": {
                "dateTime": end_datetime.isoformat(),
                "timeZone": "Asia/Jerusalem",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 30},
                ],
            },
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()
        return created_event["id"]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding lesson to calendar: {str(e)}")
    

def delete_event_from_calendar(service, google_event_id: str):
    """
    Deletes an event from Google Calendar using the event ID.
    Gracefully handles errors like event already deleted or not found.
    """
    try:
        service.events().delete(calendarId="primary", eventId=google_event_id).execute()
        return {"status": "success", "detail": "Event deleted successfully"}

    except HttpError as e:
        raise HTTPException(status_code=404, detail=f'Event not found {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting event from calendar: {str(e)}")
        

# -------------------- Maps API --------------------

def calculate_travel_time(origin, destination, departure_time):
    """
    Calculate the estimated travel time from origin to destination at a specific departure time.
    """
    try:
        gmaps = googlemaps.Client(key=Google_API_KEY)
        
        # Get directions data
        directions = gmaps.directions(
            origin,
            destination,
            mode="driving",  # Can be "walking", "bicycling", or "transit"
            departure_time=departure_time
        )

        if not directions:
            raise ValueError("No directions found.")

        try:
            duration_seconds = directions[0]['legs'][0]['duration']['value']
            duration_minutes = duration_seconds // 60  # Convert seconds to minutes
            return duration_minutes
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(f"Invalid response format from Google Maps API: {str(e)}")

    except googlemaps.exceptions.ApiError as e:
        raise HTTPException(status_code=500, detail=f"Google Maps API error: {str(e)}")
    
    except googlemaps.exceptions.TransportError as e:
        raise HTTPException(status_code=500, detail=f"Google Maps connection error: {str(e)}")
    
    except googlemaps.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Google Maps HTTP error: {str(e)}")

    except googlemaps.exceptions.Timeout as e:
        raise HTTPException(status_code=504, detail=f"Google Maps request timeout: {str(e)}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error calculating travel time: {str(e)}")


def calculate_departure_time(origin, destination, arrival_time):
    """ 
    Calculate the departure time from location_A to location_B to arrive at location_B by the given arrival_time.
    """
    try:
        arrival_time_unix = int(arrival_time.timestamp())
        gmaps = googlemaps.Client(key=Google_API_KEY)

        # Request directions with arrival_time
        directions = gmaps.directions(
            origin=origin,
            destination=destination,
            mode="driving",  # Can be "walking", "transit", or "bicycling" 
            arrival_time=arrival_time_unix  # Must be an integer 
        )

        if not directions:
            raise ValueError("No route found between the given locations.")

        try:
            # Extract travel duration in seconds
            travel_time_seconds = directions[0]['legs'][0]['duration']['value']
            departure_time = arrival_time - timedelta(seconds=travel_time_seconds)
            return departure_time.strftime("%Y-%m-%d %H:%M:%S")
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(f"Invalid response format from Google Maps API: {str(e)}")

    except googlemaps.exceptions.ApiError as e:
        raise HTTPException(status_code=500, detail=f"Google Maps API error: {str(e)}")
    
    except googlemaps.exceptions.TransportError as e:
        raise HTTPException(status_code=500, detail=f"Google Maps connection error: {str(e)}")
    
    except googlemaps.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Google Maps HTTP error: {str(e)}")

    except googlemaps.exceptions.Timeout as e:
        raise HTTPException(status_code=504, detail=f"Google Maps request timeout: {str(e)}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error calculating departure time: {str(e)}")

    
