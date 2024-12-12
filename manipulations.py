import requests
import pandas as pd

try:
    # Fetch the vehicle data
    vehicle_api = requests.get('http://127.0.0.1:8000/vehicles/')
    vehicle_api.raise_for_status()
    vehicle_api_data = vehicle_api.json()

    # Fetch the driver data
    driver_api = requests.get('http://127.0.0.1:8000/drivers/')
    driver_api.raise_for_status()
    driver_api_data = driver_api.json()
    
    
    # Convert API data to DataFrames
    vehicle_df = pd.DataFrame(vehicle_api_data['vehicles'])
    driver_df = pd.DataFrame(driver_api_data['drivers'])


    # dataframe shape

    print(f"Vehicle DataFrame shape (rows, columns): {vehicle_df.shape}")
    print(f"Drivers DataFrame shape (rows, columns): {driver_df.shape}")


    # 2. Describe the datasets
    print("\nVehicle DataFrame Description:")
    print(vehicle_df.describe(include='all'))

    print("\nDriver DataFrame Description:")
    print(driver_df.describe(include='all'))


    # Merge DataFrames for more insights
    merged_df = pd.merge(vehicle_df, driver_df, how="left", left_index=True, right_index=True)

    print("\nMerged DataFrame:")
    print(merged_df.head())

    print("\nMerged DataFrame shape with duplicates:")
    print(merged_df.shape)

         
    # 3. Data Cleaning 
    vehicle_df.dropna(subset=['name', 'license_plate'], inplace=True)
    driver_df.fillna({"name": "Unknown", "license_number": "Unknown"}, inplace=True)

    vehicle_df['created_at'] = pd.to_datetime(vehicle_df['created_at'], errors='coerce')
    driver_df['hired_at'] = pd.to_datetime(driver_df['hired_at'], errors='coerce')

    # 4. Preprocessing

    print("\nBefore removing duplicates:")
    print(f"Vehicle DataFrame - Duplicate Rows: {vehicle_df.duplicated().sum()}")
    print(f"Driver DataFrame - Duplicate Rows: {driver_df.duplicated().sum()}")

    # Remove duplicates based on the 'license_plate' and 'name' (or other critical columns)
    vehicle_df = vehicle_df.drop_duplicates(subset=['license_plate'], keep='first')  # Keep the first occurrence
    driver_df = driver_df.drop_duplicates(subset=['license_number'], keep='first')  # Keep the first occurrence

    print("\nAfter removing duplicates:")
    print(f"Vehicle DataFrame - Duplicate Rows: {vehicle_df.duplicated().sum()}")
    print(f"Driver DataFrame - Duplicate Rows: {driver_df.duplicated().sum()}")

    # # 5. Feature Engineering
    # vehicle_df['vehicle_age'] = (pd.Timestamp.now() - vehicle_df['created_at']).dt.days // 365
    # vehicle_df['short_name'] = vehicle_df['name'].apply(lambda x: x.split()[0] if isinstance(x, str) else 'Unknown')
    # driver_df['vehicle_work_time'] = (pd.Timestamp.now() - driver_df['hired_at']).dt.days // 365
    # driver_df['short_name'] = driver_df['name'].apply(lambda x: x.split()[0] if isinstance(x, str) else 'Unknown')


  
    # 6. import to CSV

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

except ValueError as ve:
    print(f"ValueError: {ve}")

except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
