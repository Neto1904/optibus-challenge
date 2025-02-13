from database.dataframe import read_dataset, create_normalized_dataframe, create_dataframe, concat_dataframes
from modules.reports.services.breaks_service import get_breaks
from modules.reports.services.duty_times_service import get_duty_times
from modules.reports.services.start_stop_description_service import get_start_stop_description
    
def main():
    file_path = "src/database/mini_json_dataset.json"
    dataset = read_dataset(file_path) 

    stops_df = create_dataframe(dataset, "stops")
    trips_df = create_dataframe(dataset, "trips")
    vehicles_df = create_normalized_dataframe(dataset, "vehicles", "vehicle_id", "vehicle_events")
    duties_df = create_normalized_dataframe(dataset, "duties", "duty_id", "duty_events")


    vehicles_time_df = vehicles_df[["duty_id", "start_time", "end_time"]]
    duties_time_df = duties_df[["duty_id", "start_time", "end_time"]]
    concated_df = concat_dataframes(vehicles_time_df, duties_time_df)

    duty_times_df = get_duty_times(concated_df)
    descriptions_df = get_start_stop_description(duty_times_df, trips_df, vehicles_df, stops_df)
    breaks_info_df = get_breaks(descriptions_df, vehicles_df, stops_df)

    print(duty_times_df, descriptions_df, breaks_info_df)

    
    

main()
