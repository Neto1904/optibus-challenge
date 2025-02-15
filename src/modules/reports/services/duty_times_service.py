
from datetime import timedelta
import pandas as pd

def parse_df_times(df):
    parsed_df = df.copy()

    parsed_df[["start_day", "start_time"]] = parsed_df["start_time"].str.split(".", expand=True)
    parsed_df[["end_day", "end_time"]] = parsed_df["end_time"].str.split(".", expand=True)

    # Calculate the number of days between the start and end time
    parsed_df["days_of_difference"] = parsed_df["end_day"].astype(int) - parsed_df["start_day"].astype(int)
    
    parsed_df["start_time"] = pd.to_datetime(parsed_df["start_time"])
    parsed_df["end_time"] = pd.to_datetime(parsed_df["end_time"])

    # Add the number of days to the 'end_time' 
    parsed_df["end_time"] = parsed_df.apply(lambda row: row['end_time'] + timedelta(days=row['days_of_difference']), axis=1)
    return parsed_df

def get_duty_times(df):
    duty_vehicles_df = df.copy()
    # Remove rows with missing values in the 'start_time' column
    duty_vehicles_df = duty_vehicles_df.dropna(subset=['start_time'])
    duty_vehicles_df = duty_vehicles_df.dropna(subset=['end_time'])

    duty_vehicles_df = parse_df_times(duty_vehicles_df)

    min_max_time_df = duty_vehicles_df.groupby("duty_id", as_index=False).agg({
        "start_time": "min", 
        "end_time": "max",
    })

    min_max_time_df["start_time"] = pd.to_datetime(min_max_time_df["start_time"]).dt.time
    min_max_time_df["end_time"] = pd.to_datetime(min_max_time_df["end_time"]).dt.time
    return min_max_time_df
