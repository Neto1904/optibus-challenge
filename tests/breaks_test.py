import pandas as pd
import pytest

from src.modules.reports.services.breaks_service import check_is_sequential, get_break_info, get_breaks

def test_get_break_info():
    data = {
        "duty_id": [1, 1],
        "start_time": ["2023-10-01 08:00:00", "2023-10-01 09:00:00"],
        "end_time": ["2023-10-01 08:30:00", "2023-10-01 09:30:00"],
        "destination_stop_id": [1, 2],
        "vehicle_event_sequence": [1, 2],
    }
    df = pd.DataFrame(data)
    dfs = [df]

    expected_break_durations = [30.0]
    expected_duty_ids = [1]
    expected_stop_ids = [1]
    expected_break_times = [pd.to_datetime("2023-10-01 09:00:00").time()]

    break_durations, duty_ids, stop_ids, break_times = get_break_info(dfs)

    assert break_durations == expected_break_durations
    assert duty_ids == expected_duty_ids
    assert stop_ids == expected_stop_ids
    assert break_times == expected_break_times

def test_get_breaks():
    descriptions_data = {
        "duty_id": [1],
        "start_time": ["08:00:00"],
        "end_time": ["18:00:00"],
        "first_stop_description": ["Stop A"],
        "last_stop_description": ["Stop B"],
    }
    descriptions_df = pd.DataFrame(descriptions_data)

    vehicles_data = {
        "duty_id": [1, 1],
        "vehicle_event_type": ["deadhead", "deadhead"],
        "start_time": ["0.08:00", "0.09:00"],
        "end_time": ["0.08:30", "0.09:30"],
        "destination_stop_id": [1, 2],
        "vehicle_event_sequence": [1, 2],
    }
    vehicles_df = pd.DataFrame(vehicles_data)

    stops_data = {
        "stop_id": [1, 2],
        "stop_name": ["Stop A", "Stop B"],
    }
    stops_df = pd.DataFrame(stops_data)

    expected_data = {
        "duty_id": [1],
        "start_time": ["08:00:00"],
        "end_time": ["18:00:00"],
        "first_stop_description": ["Stop A"],
        "last_stop_description": ["Stop B"],
        "break_start_time": [pd.to_datetime("2023-10-01 09:00:00").time()],
        "break_duration": [30.0],
        "break_stops_name": ["Stop A"],
    }

    expected_df = pd.DataFrame(expected_data)
    result_df = get_breaks(descriptions_df, vehicles_df, stops_df)

    pd.testing.assert_frame_equal(result_df, expected_df)

if __name__ == "__main__":
    pytest.main([__file__])