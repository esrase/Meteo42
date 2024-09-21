import requests
import cfgrib
import pandas as pd
from geopy.distance import geodesic
import numpy as np
from districts import districts

# Function to download GFS data from NOAA
def download_gfs_data(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Data was successfully downloaded to  {file_path}")
    else:
        print(f"Data download failed. Status code:{response.status_code}")

#Function that processes data and matches it with districts
def prepare_precipitation_data(file_path, districts):
    try:
        ds = cfgrib.open_dataset(file_path)
        prate = ds.prate
        df = prate.to_dataframe().reset_index()

        district_precipitation = {}
        for district, coordinates in districts.items():
            df['distance'] = df.apply(lambda row: geodesic(coordinates, (row['latitude'], row['longitude'])).km, axis=1)
            nearest_data = df[df['distance'] < 15]  # 15 km 
            avg_prate = nearest_data['prate'].mean()

            # If nan then set it to 0
            if np.isnan(avg_prate):
                avg_prate = 0.0

            district_precipitation[district] = avg_prate

        # Print district rainfall data on screen in a more readable way
        print("\nİlçe Yağış Verileri (mm):")
        for district, prate in district_precipitation.items():
            print(f"{district}: {prate:.6f} mm")

        return district_precipitation
    except FileNotFoundError as e:
        print(f"Dosya bulunamadı: {e}")
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
        return {}

# To save precipitation data to a CSV file:
def save_precipitation_to_csv(district_precipitation):
    df_precipitation = pd.DataFrame(list(district_precipitation.items()), columns=['District', 'Precipitation (mm)'])
    df_precipitation.to_csv('district_precipitation.csv', index=False)
    print("\nPrecipitation data was recorded in the district_precipitation.csv file.")