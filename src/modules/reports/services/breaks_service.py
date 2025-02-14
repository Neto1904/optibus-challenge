import pandas as pd  
from src.database.dataframe import join_dataframes, split_dataframe
from src.modules.reports.services.duty_times_service import parse_df_times
from src.modules.reports.services.start_stop_description_service import get_stop_description

def get_breaks(descriptions_df, vehicles_df, stops_df):
    break_duration_list, duty_ids_list, break_stops_name, break_start_times = [], [], [], []

    for index, row in descriptions_df.iterrows():
        vehicles_df_filtered = filter_vehicles_df(vehicles_df, row["duty_id"])
        if vehicles_df_filtered.empty:
            continue

        parsed_df_times = parse_df_times(vehicles_df_filtered)
        splitted_dfs = split_dataframe(parsed_df_times, 2)
        break_durations, duty_ids, stop_ids, break_times = get_break_info(splitted_dfs)
        stops_descriptions = [get_stop_description(stop_id, stops_df) for stop_id in stop_ids]

        break_duration_list.extend(break_durations)
        duty_ids_list.extend(duty_ids)
        break_stops_name.extend(stops_descriptions)
        break_start_times.extend(break_times)


    breaks_info = create_breaks_info_df(break_duration_list, duty_ids_list, break_stops_name, break_start_times)
    joined_df = join_dataframes(breaks_info, descriptions_df, "duty_id")
    return joined_df[["duty_id", "start_time", "end_time", "first_stop_description", "last_stop_description", "break_start_time","break_duration", "break_stops_name"]]

def filter_vehicles_df(vehicles_df, duty_id):
    return vehicles_df[(vehicles_df["duty_id"] == duty_id) & (vehicles_df["vehicle_event_type"] == "deadhead")]

def create_breaks_info_df(break_duration_list, duty_ids_list, break_stops_name, break_start_times):
    return pd.DataFrame({
        "break_duration": break_duration_list,
        "duty_id": duty_ids_list,
        "break_stops_name": break_stops_name,
        "break_start_time": break_start_times
    })

def check_is_sequential(df):
    # check if the deadhead events are sequential
    first_event = df["vehicle_event_sequence"].astype(int).head(1).values[0]
    second_event = df["vehicle_event_sequence"].astype(int).tail(1).values[0]
    return second_event - first_event == 1 
       

def get_break_info(dfs):
    break_durations, duty_ids, stop_ids, break_times = [], [], [], []

    for df in dfs:
        if not check_is_sequential(df): 
            continue

        first_duty_end_time = df["end_time"].head(1).values[0]
        second_duty_start_time = df["start_time"].tail(1).values[0]
        duty_id = df["duty_id"].head(1).values[0]
        stop_id = df["destination_stop_id"].head(1).values[0]
        break_duration = pd.to_datetime(second_duty_start_time) - pd.to_datetime(first_duty_end_time)
        break_duration_minutes = break_duration.total_seconds() / 60

        if break_duration_minutes > 15.00:
            break_durations.append(break_duration_minutes)
            duty_ids.append(duty_id)
            stop_ids.append(stop_id)
            break_times.append(pd.to_datetime(second_duty_start_time).time())

    return break_durations, duty_ids, stop_ids, break_times
