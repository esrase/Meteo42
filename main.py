from data_preparation import download_gfs_data, prepare_precipitation_data, save_precipitation_to_csv
from map_creation import create_weather_map
from districts import districts

# URL to pull data from NOAA
url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.20240921%2F00%2Fatmos&file=gfs.t00z.pgrb2.0p25.anl&var_PRATE=on&lev_surface=on&subregion=&toplat=40&leftlon=31&rightlon=35&bottomlat=36"
file_path = "gfs_data.grb2"

# GeoJSON file
geojson_file = "13_202103_ilceler (3).geojson"

# 1. Download data
download_gfs_data(url, file_path)

# 2. Data preparation
district_precipitation = prepare_precipitation_data(file_path, districts)

# 3. Saving data to CSV file
save_precipitation_to_csv(district_precipitation)

# 4. Creating a map
create_weather_map(district_precipitation, geojson_file)