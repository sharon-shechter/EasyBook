import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, date
from backend.services.lessonService import (
    create_lesson,
    round_to_nearest_five,
    get_possible_time_slots
)
from backend.models.lessonModel import Lesson
from backend.schemas.lessonSchema import LessonCreate, LessonResponse
import pytz

tz = pytz.timezone("Asia/Jerusalem")

# ---------- MOCK FIXTURES ----------
@pytest.fixture
def mock_db_session():
    """Mock SQLAlchemy session."""
    mock_db = MagicMock()
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    return mock_db

@pytest.fixture
def sample_lesson_data():
    """Sample lesson creation data."""
    return LessonCreate(
        date=date.today(),
        start_time=datetime.now(tz).time(),  # Convert to `time` type
        end_time=(datetime.now(tz) + timedelta(hours=1)).time(),  # Convert to `time` type
        location="Tel Aviv",
        adress="123 Main St",
        status=1,  # Ensure integer value
        lesson_name="Math Class",
        class_number="101",
        duration=60  # Ensure required field is present
    )

@pytest.fixture
def sample_events():
    """Mock Google Calendar events."""
    return [
        {
            "start": {"dateTime": (datetime.now(tz) + timedelta(hours=1)).isoformat()},
            "end": {"dateTime": (datetime.now(tz) + timedelta(hours=2)).isoformat()},
            "location": "Jerusalem"
        }
    ]

# ---------- TESTS ----------

def test_create_lesson(mock_db_session, sample_lesson_data):
    """Test lesson creation with mock database."""
    user_id = 1
    lesson_response = create_lesson(mock_db_session, sample_lesson_data, user_id)

    print("Lesson Response:", lesson_response)  # Debugging output

    # Ensure response is not an error response
    assert lesson_response.status_code == 200, f"Unexpected response: {lesson_response}"

    # Ensure the response contains expected fields
    assert isinstance(lesson_response, LessonResponse)
    assert lesson_response.user_id == user_id
    assert lesson_response.date == sample_lesson_data.date
    assert lesson_response.start_time == sample_lesson_data.start_time
    assert lesson_response.end_time == sample_lesson_data.end_time
    assert lesson_response.lesson_type  == sample_lesson_data.location
    assert lesson_response.home_adress == sample_lesson_data.adress
    assert lesson_response.status == sample_lesson_data.status
    assert lesson_response.lesson_name == sample_lesson_data.lesson_name
    assert lesson_response.class_number == sample_lesson_data.class_number

def test_round_to_nearest_five():
    """Test rounding function."""
    test_time = datetime(2025, 3, 6, 14, 7, 45)  # 14:07:45
    rounded_time = round_to_nearest_five(test_time)
    assert rounded_time.minute == 5  # Should round down to 14:05

    test_time = datetime(2025, 3, 6, 14, 13, 30)  # 14:13:30
    rounded_time = round_to_nearest_five(test_time)
    assert rounded_time.minute == 15  # Should round up to 14:15

def test_get_possible_time_slots(sample_events):
    """Test available time slots calculation."""
    lesson_date = date.today()
    lesson_address = "123 Main St"
    lesson_duration = 60  # 1 hour

    with patch("backend.services.Google_apiService.calculate_departure_time", 
               return_value=(datetime.now(tz) - timedelta(minutes=30)).isoformat()):
        with patch("backend.services.Google_apiService.calculate_travel_time", return_value=30):
            with patch("backend.services.Google_apiService.is_time_slot_available", return_value=True):
                slots = get_possible_time_slots(lesson_date, lesson_address, lesson_duration, sample_events)

    assert isinstance(slots, list), "Slots should be a list"
    assert len(slots) > 0, "There should be at least one available slot"
    assert isinstance(slots[0], tuple), "Each slot should be a tuple"
