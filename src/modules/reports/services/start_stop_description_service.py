
def get_start_stop_description(duty_times_df, trips_df, vehicles_df, stops_df):
    first_stops_description, last_stops_description = [], []

    for index, row in duty_times_df.iterrows():
        filtered_vehicles_df = vehicles_df[(vehicles_df["duty_id"] == row["duty_id"]) & (vehicles_df["vehicle_event_type"] == "service_trip")]
        if filtered_vehicles_df.empty:
            continue     
        
        # Get first and last trip id
        first_trip_id = filtered_vehicles_df.head(1)["trip_id"].values[0]
        last_trip_id = filtered_vehicles_df.tail(1)["trip_id"].values[0]

        # Get first and last trip
        first_trip = trips_df[trips_df["trip_id"] == first_trip_id]
        last_trip = trips_df[trips_df["trip_id"] == last_trip_id]

        if first_trip.empty:
            first_stops_description.append('No description')

        if first_trip.empty and last_trip.empty:
            last_stops_description.append('No description')
            continue

        # Get first and last stop id
        first_stop_id = first_trip["origin_stop_id"].values[0]
        last_stop_id = last_trip["destination_stop_id"].values[0]

        # Get first and last stop description
        first_stop_description = get_stop_description(first_stop_id, stops_df)
        last_stop_description = get_stop_description(last_stop_id, stops_df)

        # Append to list
        first_stops_description.append(first_stop_description)
        last_stops_description.append(last_stop_description)

    descriptions_df = duty_times_df.copy()
    
    # Add columns to dataframe
    print(first_stops_description)
    print(last_stops_description)
    descriptions_df["first_stop_description"] = first_stops_description
    descriptions_df["last_stop_description"] = last_stops_description
    return descriptions_df  

def get_stop_description(stop_id, stops_df):
    if stops_df[stops_df["stop_id"] == stop_id].empty:
        return "No description"
    return stops_df[stops_df["stop_id"] == stop_id]["stop_name"].values[0]
