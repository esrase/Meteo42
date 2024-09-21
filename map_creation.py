import folium
import json
import webbrowser
from districts import districts


def create_weather_map(district_precipitation, geojson_file):
    map_center = [37.8713, 32.4846]  #Konya city center
    konya_map = folium.Map(location=map_center, zoom_start=10)

    # Read GeoJSON file
    with open(geojson_file, 'r', encoding='Windows-1252') as f:
        geojson_data = json.load(f)

    #Add GeoJSON data to map
    folium.GeoJson(geojson_data,
                   name='geojson',
                   style_function=lambda x: {'color': 'blue', 'weight': 2.5}).add_to(konya_map)

    for district, coordinates in districts.items():
        precipitation = district_precipitation.get(district, 0)

        # Set icon color according to precipitation amount
        if precipitation > 1.0:
            ikon = folium.Icon(color="blue", icon="fa-cloud-rain", prefix='fa')
        elif precipitation > 0.5:
            ikon = folium.Icon(color="lightblue", icon="fa-cloud", prefix='fa')
        else:
            ikon = folium.Icon(color="orange", icon="fa-sun", prefix='fa')

        # Show precipitation value in 6 digits
        folium.Marker([coordinates[0], coordinates[1]], popup=f"{district}: {precipitation:.6f} mm", icon=ikon).add_to(konya_map)

    konya_map.save("konya_weather_map.html")
    webbrowser.open("konya_weather_map.html")