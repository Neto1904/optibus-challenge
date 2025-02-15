from src.database.dataframe import read_dataset, create_normalized_dataframe, create_dataframe, concat_dataframes
from src.modules.reports.services.breaks_service import get_breaks
from src.modules.reports.services.duty_times_service import get_duty_times
from src.modules.reports.services.start_stop_description_service import get_start_stop_description
from src.utils.wirite_file import write_dataframe_to_csv

def generate_duty_times_report(vehicles_duties_df, trips_df, vehicles_df, stops_df):
    duty_times_df = get_duty_times(vehicles_duties_df)
    write_dataframe_to_csv(duty_times_df, "duty_times.csv")
    print("Duty Times Report generated: duty_times.csv")

def generate_start_stop_description_report(vehicles_duties_df, trips_df, vehicles_df, stops_df):
    duty_times_df = get_duty_times(vehicles_duties_df)
    descriptions_df = get_start_stop_description(duty_times_df, trips_df, vehicles_df, stops_df)
    write_dataframe_to_csv(descriptions_df, "descriptions_df.csv")
    print("Start/Stop Description Report generated: descriptions_df.csv")

def generate_breaks_info_report(vehicles_duties_df, trips_df, vehicles_df, stops_df):
    duty_times_df = get_duty_times(vehicles_duties_df)
    descriptions_df = get_start_stop_description(duty_times_df, trips_df, vehicles_df, stops_df)
    breaks_info_df = get_breaks(descriptions_df, vehicles_df, stops_df)
    write_dataframe_to_csv(breaks_info_df, "breaks_info_df.csv")
    print("Breaks Info Report generated: breaks_info_df.csv")

def main():
    file_path = "src/database/mini_json_dataset.json"
    dataset = read_dataset(file_path) 

    stops_df = create_dataframe(dataset, "stops")
    trips_df = create_dataframe(dataset, "trips")
    vehicles_df = create_normalized_dataframe(dataset, "vehicles", "vehicle_id", "vehicle_events")
    duties_df = create_normalized_dataframe(dataset, "duties", "duty_id", "duty_events")

    vehicles_time_df = vehicles_df[["duty_id", "start_time", "end_time"]]
    duties_time_df = duties_df[["duty_id", "start_time", "end_time"]]
    vehicles_duties_df = concat_dataframes(vehicles_time_df, duties_time_df)

    options = {
        "1": generate_duty_times_report,
        "2": generate_start_stop_description_report,
        "3": generate_breaks_info_report
    }

    while True:
        print("------------------------------------------------------")
        print("Choose an option:")
        print("1. Generate Duty Times Report")
        print("2. Generate Start/Stop Description Report")
        print("3. Generate Breaks Info Report")
        print("4. Exit")
        choice = input("Enter the number of your choice: ")

        if choice == "4":
            break

        if choice not in options:
            print("Invalid choice. Please select a valid option.")

        if choice in options:
            options[choice](vehicles_duties_df, trips_df, vehicles_df, stops_df)

main()