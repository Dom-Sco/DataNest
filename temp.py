import pandas as pd
import requests
import time

# Load CSV file
csv_file = 'temperature/temp.csv'
df = pd.read_csv(csv_file)

# This will store the first words where the last column is empty
miss_place = []
missing_data_list = []

# Get first and last column names dynamically
first_col = df.columns[0]
last_col = df.columns[-1]

# Iterate over rows
for _, row in df.iterrows():
    first_value = row[first_col]
    last_value = row[last_col]

    if pd.isna(last_value) or last_value == '':
        first_word = str(first_value).split()[0] # Get first word only
        missing_data_list.append(first_word)
        miss_place.append('first_value')

# Result
print("Missing data list:", missing_data_list, len(missing_data_list))





def get_lat_lon_osm(place_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
    "q": place_name,
    "format": "json",
    "limit": 1
    }
    headers = {
    "User-Agent": "my-osm-geocoder-app" # Required!
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            return None
    else:
        raise Exception(f"Error: {response.status_code}")


m_lat = []
m_lon = []

for place in missing_data_list:
    try:
        result = get_lat_lon_osm(place)
        if result:
            print(f"{place} → Lat: {result[0]}, Lon: {result[1]}")
            m_lat.append(result[0])
            m_lon.append(result[1])
        else:
            print(f"{place} → Not found")
    except Exception as e:
        print(f"Error for {place}: {e}")
        time.sleep(1) # Respect rate limits


def fill_missing_from_list(column, new_values):
    col_copy = column.copy()
    insert_index = 0
    for idx in range(len(col_copy)):
        if pd.isna(col_copy.iloc[idx]):
            if insert_index < len(new_values):
                col_copy.iloc[idx] = new_values[insert_index]
                insert_index += 1
    return col_copy

df['latitude'] = fill_missing_from_list(df['latitude'], m_lat)
df['longitude'] = fill_missing_from_list(df['longitude'], m_lon)

df.to_csv('temp.csv', index=False)