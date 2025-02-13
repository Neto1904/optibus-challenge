import pandas as pd
import pytest
from src.modules.reports.services.start_stop_description_service import get_start_stop_description, get_stop_description


def test_get_stop_description():
    stops_data = {
        "stop_id": [1, 2, 3],
        "stop_name": ["Stop A", "Stop B", "Stop C"],
    }
    stops_df = pd.DataFrame(stops_data)

    assert get_stop_description(1, stops_df) == "Stop A"
    assert get_stop_description(2, stops_df) == "Stop B"
    assert get_stop_description(3, stops_df) == "Stop C"

def test_get_start_stop_description():
    duty_times_data = {
        "duty_id": [1, 2],
    }
    duty_times_df = pd.DataFrame(duty_times_data)
    vehicles_data = {
        "duty_id": [1, 1, 2, 2],
        "vehicle_event_type": ["service_trip", "service_trip", "service_trip", "service_trip"],
        "trip_id": [101, 102, 201, 202],
    }
    vehicles_df = pd.DataFrame(vehicles_data)
    trips_data = {
        "trip_id": [101, 102, 201, 202],
        "origin_stop_id": [1, 2, 3, 1],
        "destination_stop_id": [2, 3, 1, 2],
    }
    trips_df = pd.DataFrame(trips_data)
    stops_data = {
        "stop_id": [1, 2, 3],
        "stop_name": ["Stop A", "Stop B", "Stop C"],
    }
    stops_df = pd.DataFrame(stops_data)
    expected_data = {
        "duty_id": [1, 2],
        "first_stop_description": ["Stop A", "Stop C"],
        "last_stop_description": ["Stop C", "Stop B"],
    }

    expected_df = pd.DataFrame(expected_data)
    result_df = get_start_stop_description(duty_times_df, trips_df, vehicles_df, stops_df)

    pd.testing.assert_frame_equal(result_df, expected_df)

# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])