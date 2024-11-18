import pandas as pd
from geopy.geocoders import Nominatim

# File paths and constants
input_file_path = "./burghs/List_of_burghs_in_Scotland_2.csv"
output_file_path = "./burghs/Updated_List_of_burghs_with_lat_long.csv"

# Initialize geocoder
geolocator = Nominatim(user_agent="geo_burgh_locator")

def fetch_coordinates(location_name):
    """Fetch latitude and longitude for a given location."""
    try:
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Error fetching coordinates for {location_name}: {e}")
    return None, None

# Read the input CSV
df = pd.read_csv(input_file_path)

# Clean the "Burgh" column and create "lat" and "long" columns
df["Burgh_Cleaned"] = df["Burgh"].str.replace(r"(?i)(royal\s*burgh|burgh)", "", regex=True).str.strip()
df["lat"], df["long"] = zip(*df["Burgh_Cleaned"].apply(fetch_coordinates))

# Save the updated dataframe to a new CSV
df.to_csv(output_file_path, index=False)

print(f"Updated file saved to {output_file_path}")
