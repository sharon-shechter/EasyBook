from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import time
import googlemaps
import pytz
from config import token, credentials, Google_API_KEY




SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


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
        raise Exception(f"Failed to retrieve events: {str(e)}")
    
def is_reasonable_time_slot(start_time, end_time):
    """Make sure the time slot is reasonable"""

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

def is_time_slot_available(events, start_time, end_time):
    """
    Check if a given time slot is available.
    """
    try: 
        if not is_reasonable_time_slot(start_time, end_time):
            return False
    except Exception as e:
        raise Exception(f"Error checking time slot resenoable: {str(e)}")
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
        raise Exception(f"Error checking time slot availability: {str(e)}")
    


        

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

        if directions:
            try:
                duration_seconds = directions[0]['legs'][0]['duration']['value']
                duration_minutes = duration_seconds // 60  # Convert seconds to minutes
                return duration_minutes
            except (KeyError, IndexError, TypeError) as e:
                return e
        else:
            return ValueError("No directions found.")

    except Exception as e:
        raise Exception(f"Error checking time slot availability: {str(e)}")

        

def calculate_departure_time(origin, destination, arrival_time):
    """ 
    Calculate the departure time from location_A to location_B to arrive at location_B by the given arrival_time.
    """
    try:
        arrival_time_unix = int(arrival_time.timestamp())
        gmaps = googlemaps.Client(key=Google_API_KEY)

        # Request directions with arrival_time

        try:
                directions = gmaps.directions(
                    origin=origin,
                    destination=destination,
                    mode="driving",  # Can be "walking", "transit", or "bicycling" 
                    arrival_time=arrival_time_unix  # Must be an integer 
                )
        except Exception as e:
            raise Exception(f"Error getting directions: {str(e)}")
        

        if not directions:
            return ValueError("No route found between the given locations.")

        # Extract travel duration in seconds
        try:
            travel_time_seconds = directions[0]['legs'][0]['duration']['value']
            departure_time = arrival_time - timedelta(seconds=travel_time_seconds)
            return departure_time.strftime("%Y-%m-%d %H:%M:%S") 
        except (KeyError, IndexError, TypeError) as e:
            return e

    except Exception as e:
        raise Exception(f"Error calculating departure time: {str(e)}")
    
