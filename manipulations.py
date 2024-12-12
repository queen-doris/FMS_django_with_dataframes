import requests
import pandas as pd

try:

    #1.Fetch API data

    # Fetch the vehicle data
    vehicle_api = requests.get('http://127.0.0.1:8000/vehicles/')
    vehicle_api.raise_for_status()
    vehicle_api_data = vehicle_api.json()

    # Fetch the driver data
    driver_api = requests.get('http://127.0.0.1:8000/drivers/')
    driver_api.raise_for_status()
    driver_api_data = driver_api.json()
    
    
    # Convert API data to DataFrames
    vehicles_list = vehicle_api_data.get('vehicles', [])
    vehicle_df = pd.DataFrame(vehicles_list)
    #  print("Vehicle DataFrame Columns:")
    print(vehicle_df.columns)

    drivers_list = driver_api_data.get('drivers', [])
    driver_df = pd.DataFrame(drivers_list)
     #  print("Driver DataFrame Columns:")
    print(driver_df.columns)

    merged_df = pd.merge(vehicle_df, driver_df, how="inner", left_index=True, right_index=True)

    print("\n\nMerged DataFrame:")
    print(merged_df.head())

    print("\n\nMerged DataFrame shape:")
    print(merged_df.shape)
    print(f"Vehicle DataFrame shape (rows, columns): {vehicle_df.shape}")
    print(f"Drivers DataFrame shape (rows, columns): {driver_df.shape}")




    # 2. Describe the datasets

    print("\n\nVehicle DataFrame Description:")
    print(vehicle_df.describe(include='all'))

    print("\n\nDriver DataFrame Description:")
    print(driver_df.describe(include='all'))

    print("\n\nMerged Dataframe Description:")
    print(merged_df.describe(include='all'))




   # 3. data cleaning

    print("\n\nVehicle DataFrame - Null Values Summary:")
    print(vehicle_df.isnull().sum())
    print("\n\nDriver DataFrame - Null Values Summary:")
    print(driver_df.isnull().sum())
    print("\n\nMerged DataFrame - Null Values Summary:")
    print(merged_df.isnull().sum())

   
    vehicle_df.dropna(inplace=True)
    driver_df.fillna("Unknown", inplace=True)
    


    # 4. Preprocessing


    print("\n\nBefore removing duplicates:")
    print(f"Vehicle DataFrame - Duplicate Rows: {vehicle_df.duplicated().sum()}")
    print(f"Driver DataFrame - Duplicate Rows: {driver_df.duplicated().sum()}")

    # Remove duplicates based on the 'license_plate' and 'name' 
    vehicle_df = vehicle_df.drop_duplicates(subset=['license_plate'], keep='first')  
    driver_df = driver_df.drop_duplicates(subset=['license_number'], keep='first')  

    print("\n\nAfter removing duplicates:")
    print(f"Vehicle DataFrame - Duplicate Rows: {vehicle_df.duplicated().sum()}")
    print(f"Driver DataFrame - Duplicate Rows: {driver_df.duplicated().sum()}")




    # 5. Feature Engineering
    
    if 'created_at' in vehicle_df.columns:
        vehicle_df['created_at'] = pd.to_datetime(vehicle_df['created_at'], errors='coerce').dt.tz_localize(None)
        current_time = pd.Timestamp.now().tz_localize(None)
        vehicle_df['vehicle_age_in_days'] = (current_time - vehicle_df['created_at']).dt.days 
        vehicle_df['vehicle_age_in_years'] = (current_time - vehicle_df['created_at']).dt.days//365 


        print("\n\nvehicles with new feature of vehicle_age:\n")
        print(vehicle_df)
  
    else:
        print("Column 'created_at' not found in vehicle_df.")
    
    if 'hired_at' in driver_df.columns:
        driver_df['hired_at'] = pd.to_datetime(driver_df['hired_at'], errors='coerce').dt.tz_localize(None)
        current_time = pd.Timestamp.now().tz_localize(None)
        driver_df['work_duration_in_days'] = (current_time - driver_df['hired_at']).dt.days
        driver_df['short_name'] = driver_df['name'].apply(lambda x: x.split()[0] if isinstance(x, str) else 'Unknown')
        
        print("\n\ndrivers with new feature of work_duration:\n")
        print(driver_df)

    else:
        print("Column 'hired_at' not found in driver_df.")

    

    #6. export my data with pagination to CSV  
    
    merged_df = pd.merge(vehicle_df, driver_df, how="inner", left_index=True, right_index=True)
    print("\n\n New merged dataframe with new features:")
    print(merged_df)
    print("\n\nEXPORTING DATA TO CSV .....")
    merged_df.to_csv('final_merged_data.csv', index=False)
    print("Final merged DataFrame has been exported to 'final_merged_data.csv'")



    # 7. export to CSV for data without pagination

    # driver_df.iloc[:50].to_csv('driver_1.csv', index=False, mode='w', header=True)
    # print("Exported first 50 drivers to drivers_1.csv")

    # # Export the next 50 drivers
    # driver_df.iloc[50:100].to_csv('driver_2.csv', index=False, mode='w', header=True)
    # print("Exported next 50 drivers to drivers_2.csv")

    # # Read the two CSV files into DataFrames
    # driver_df1 = pd.read_csv('driver_1.csv')
    # driver_df2 = pd.read_csv('driver_2.csv')
    
    # merged_df = pd.concat([driver_df1, driver_df2], ignore_index=True)

    # merged_df.to_csv('final_drivers.csv', index=False)
    # print("Merged both chunks into final_drivers.csv")
    
    # # Exporting first 50 drivers with specific attributes 
    # df_part1 = driver_df[['name', 'license_number']].iloc[:50]
    # df_part1.to_csv('drivers_part1.csv', index=False, mode='w', header=True)
    # print("Exported first 50 drivers with 'name' and 'license_number' to drivers_part1.csv")

    # df_part2 = driver_df[['hired_at', 'assigned_vehicle']].iloc[50:100]
    # df_part2.to_csv('drivers_part2.csv', index=False, mode='w', header=True)
    # print("Exported next 50 drivers with 'hire date' and 'vehicles' to drivers_part2.csv")

    # df1_part = pd.read_csv('drivers_part1.csv')
    # df2_part = pd.read_csv('drivers_part2.csv')

    # combined_parts = pd.concat([df1_part, df2_part], axis=1)

    # combined_parts.to_csv('final_parts_drivers.csv', index=False)
    # print("Merged both parts into final_parts_drivers.csv")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
         


