import pandas as pd
from datetime import time, timedelta
import pytest
from src.modules.reports.services.duty_times_service import get_duty_times, parse_df_times



def test_parse_df_times():
    data = {
        "start_time": ["1.08:00:00", "2.09:00:00", "3.10:00:00"],
        "end_time": ["1.08:30:00", "3.09:30:00", "5.10:30:00"],
    }
    df = pd.DataFrame(data)

    # Expected output
    expected_data = {
        "start_time": [
            pd.to_datetime("08:00:00"),
            pd.to_datetime("09:00:00"),
            pd.to_datetime("10:00:00"),
        ],
        "end_time": [
            pd.to_datetime("08:30:00"),
            pd.to_datetime("09:30:00") + timedelta(days=1),
            pd.to_datetime("10:30:00") + timedelta(days=2),
        ],
        "start_day": ["1", "2", "3"],
        "end_day": ["1", "3", "5"],
        "days_of_difference": [0, 1, 2],
    }
    expected_df = pd.DataFrame(expected_data)

    result_df = parse_df_times(df)
    pd.testing.assert_frame_equal(result_df, expected_df)

def test_get_duty_times():
    data = {
        "duty_id": [1, 1, 2, 2, 3],
        "start_time": [
            "1.08:00:00", 
            "1.09:00:00", 
            "2.10:00:00", 
            None,  # Missing start_time (should be dropped)
            "3.12:00:00"
        ],
        "end_time": [
            "1.08:30:00", 
            "1.09:30:00", 
            "2.10:30:00", 
            "2.11:30:00", 
            "3.12:30:00"
        ],
    }
    df = pd.DataFrame(data)

    # Expected output
    expected_data = {
        "duty_id": [1, 2, 3],
        "start_time": [time(8, 0), time(10, 0), time(12, 0)],
        "end_time": [time(9, 30), time(10, 30), time(12, 30)],
    }

    expected_df = pd.DataFrame(expected_data)
    result_df = get_duty_times(df)
    pd.testing.assert_frame_equal(result_df, expected_df)

if __name__ == "__main__":
    pytest.main([__file__])