import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, date
import pytz
from backend.services.Google_apiService import (
    authenticate_google_calendar,
    get_events_of_date,
    is_time_slot_available,
    calculate_travel_time,
    calculate_departure_time
)

tz = pytz.timezone("Asia/Jerusalem")

# ---------- MOCKS ----------
@pytest.fixture
def mock_google_service():
    """Mock Google Calendar API service."""
    mock_service = MagicMock()
    mock_service.events().list().execute.return_value = {"items": []}  # No events initially
    return mock_service


@pytest.fixture
def sample_events():
    """Mock event data from Google Calendar."""
    return [
        {
            "start": {"dateTime": (datetime.now(tz) + timedelta(hours=1)).isoformat()},
            "end": {"dateTime": (datetime.now(tz) + timedelta(hours=2)).isoformat()},
        },
        {
            "start": {"dateTime": (datetime.now(tz) + timedelta(hours=4)).isoformat()},
            "end": {"dateTime": (datetime.now(tz) + timedelta(hours=5)).isoformat()},
        },
    ]


# ---------- TESTS ----------
def test_authenticate_google_calendar():
    """Test that the authentication function initializes without crashing."""
    with patch("backend.services.Google_apiService.build", return_value=MagicMock()) as mock_build:
        service = authenticate_google_calendar()
        assert service is not None
        mock_build.assert_called()


def test_get_events_of_date(mock_google_service):
    """Test fetching events from Google Calendar for a specific date."""
    test_date = date.today()
    
    with patch("backend.services.Google_apiService.build", return_value=mock_google_service):
        events = get_events_of_date(mock_google_service, test_date)
    
    assert isinstance(events, list)


@pytest.mark.parametrize(
    "start_time, end_time, expected",
    [
        (datetime.now(tz), datetime.now(tz) + timedelta(hours=1), True),  # No conflict
        (datetime.now(tz) + timedelta(hours=1), datetime.now(tz) + timedelta(hours=2), False),  # Overlaps event
        (datetime.now(tz) + timedelta(hours=3), datetime.now(tz) + timedelta(hours=4), True),  # Free slot
        (datetime.now(tz) + timedelta(hours=4, minutes=30), datetime.now(tz) + timedelta(hours=5, minutes=30), False),  # Overlaps
    ],
)
def test_is_time_slot_available(sample_events, start_time, end_time, expected):
    """Test checking if a time slot is available."""
    result = is_time_slot_available(sample_events, start_time, end_time)
    assert result == expected


@patch("backend.services.Google_apiService.googlemaps.Client")
def test_calculate_travel_time(mock_googlemaps):
    """Test calculating travel time."""
    mock_gmaps = MagicMock()
    mock_gmaps.directions.return_value = [{"legs": [{"duration": {"value": 1800}}]}]  # 30 minutes
    mock_googlemaps.return_value = mock_gmaps

    travel_time = calculate_travel_time("Tel Aviv", "Jerusalem", datetime.now())
    assert travel_time == 30  # Minutes


@patch("backend.services.Google_apiService.googlemaps.Client")
def test_calculate_departure_time(mock_googlemaps):
    """Test calculating departure time."""
    mock_gmaps = MagicMock()
    mock_gmaps.directions.return_value = [{"legs": [{"duration": {"value": 3600}}]}]  # 1 hour
    mock_googlemaps.return_value = mock_gmaps

    arrival_time = datetime.now() + timedelta(hours=3)
    departure_time = calculate_departure_time("Tel Aviv", "Jerusalem", arrival_time)

    expected_departure = arrival_time - timedelta(hours=1)
    assert departure_time == expected_departure.strftime("%Y-%m-%d %H:%M:%S")
