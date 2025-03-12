import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz
from backend.schemas.lessonSchema import LessonCreate  # Import your LessonCreate model


from backend.services.lessonService import (
    create_lesson_service,
    delete_lesson_service,
    round_to_nearest_five,
    generate_full_day_slots,
    get_possible_time_slots
)

# Mock dependencies
@pytest.fixture
def mock_db():
    """Mock SQLAlchemy database session."""
    return MagicMock(spec=Session)

@pytest.fixture
def mock_google_service():
    """Mock Google API service."""
    return MagicMock()

def test_create_lesson_service(mock_db, mock_google_service):
    """Test successful lesson creation via service logic."""
    lesson_data = MagicMock(spec=LessonCreate)  
    lesson_data.date = datetime(2025, 3, 15).date()
    lesson_data.start_time = datetime(2025, 3, 15, 10, 0).time()
    lesson_data.end_time = datetime(2025, 3, 15, 11, 0).time()
    user_id = 1
    status = 1

    mock_user = MagicMock()
    mock_user.first_name = "John"
    mock_user.last_name = "Doe"

    with patch("backend.services.Google_apiService.add_lesson_to_calendar", return_value="mock_google_event_id"), \
         patch("backend.repositories.lessonRepositorie.create_lesson", return_value={"id": 123, "google_event_id": "mock_google_event_id"}), \
         patch("backend.services.userService.get_user_by_id", return_value=mock_user):  # ✅ Mock user

        lesson = create_lesson_service(mock_db, lesson_data, user_id, status, mock_google_service)

    assert lesson["id"] == 123
    assert lesson["google_event_id"] == "mock_google_event_id"



def test_delete_lesson_service(mock_db, mock_google_service):
    """Test successful deletion of lesson through service logic."""
    lesson_id = 1
    user_id = 1
    mock_lesson = MagicMock() 
    mock_lesson.google_event_id = "mock_google_event_id"

    with patch("backend.repositories.lessonRepositorie.get_lessons_by_lesson_id", return_value=mock_lesson), \
         patch("backend.services.Google_apiService.delete_event_from_calendar") as mock_delete_event, \
         patch("backend.repositories.lessonRepositorie.delete_lesson_from_db") as mock_delete_lesson:

        result = delete_lesson_service(lesson_id, user_id, mock_google_service, mock_db)

    mock_delete_event.assert_called_once_with(mock_google_service, "mock_google_event_id")
    mock_delete_lesson.assert_called_once_with(mock_db, lesson_id)
    assert result is True


def test_round_to_nearest_five():
    """Test rounding function for datetime rounding to nearest 5 minutes."""
    dt1 = datetime(2025, 3, 15, 10, 7, 45)  # ✅ Should round to 10:10
    rounded_dt1 = round_to_nearest_five(dt1)
    assert rounded_dt1.minute == 10

    dt2 = datetime(2025, 3, 15, 10, 3)  # ✅ Should round to 10:05
    rounded_dt2 = round_to_nearest_five(dt2)
    assert rounded_dt2.minute == 5

    dt3 = datetime(2025, 3, 15, 10, 8)  # ✅ Should round to 10:10
    rounded_dt3 = round_to_nearest_five(dt3)
    assert rounded_dt3.minute == 10


def test_generate_full_day_slots():
    """Test function to generate full-day time slots."""
    lesson_date = datetime(2025, 3, 15).date()
    lesson_duration = 60  # 1 hour lessons

    slots = generate_full_day_slots(lesson_date, lesson_duration)

    assert len(slots) > 0
    assert slots[0][0].hour == 8  # First slot starts at 8:00 AM
    assert slots[-1][1].hour <= 21  # Last slot ends by 9:00 PM


def test_get_possible_time_slots():
    """Test available time slot generation considering travel constraints."""
    lesson_address = "Student's Home"
    lesson_duration = 60  # 1 hour

    mock_events = [
        {"start": {"dateTime": "2025-03-15T12:00:00+02:00"}, "end": {"dateTime": "2025-03-15T13:00:00+02:00"}, "location": "Library"},
    ]

    with patch("backend.services.Google_apiService.calculate_departure_time", return_value="2025-03-15T11:30:00+02:00"), \
         patch("backend.services.Google_apiService.calculate_travel_time", return_value=30), \
         patch("backend.services.Google_apiService.is_time_slot_available", return_value=True):

        available_slots = get_possible_time_slots(lesson_address, lesson_duration, mock_events)

    assert len(available_slots) > 0  # ✅ Should return at least one available slot