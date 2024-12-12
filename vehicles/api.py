import requests
import pandas as pd

inner_merged_df = None
try:
    vehicle_api = requests.get('http://localhost:8000/vehicles/')
    vehicle_api.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    vehicle_api_data = vehicle_api.json()
    vehicle_owners_api = requests.get('http://localhost:8000/drivers/')
    vehicle_owners_api.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    vehicle_owners_api_data = vehicle_owners_api.json()
    vdf = pd.DataFrame(vehicle_api_data['vehicles'])
    odf = pd.DataFrame(vehicle_owners_api_data['drivers'])

    inner_merged_df = pd.merge(vdf, odf, on="id", how="inner")
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")




