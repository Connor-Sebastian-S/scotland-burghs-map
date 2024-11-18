import os
import pandas as pd
from geopy.geocoders import Nominatim

# Directory containing input CSV files and output consolidated CSV
input_directory = "./burghs"
output_file = "./consolidated_burghs.csv"

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

# Create an empty DataFrame to hold consolidated data
consolidated_df = pd.DataFrame()

# Process each CSV file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_directory, file_name)
        
        # Read the current CSV file
        print(f"Processing file: {file_name}")
        df = pd.read_csv(file_path)

        # Clean the "Burgh" column
        df["Burgh_Cleaned"] = df["Burgh"].str.replace(r"(?i)(royal\s*burgh|burgh)", "", regex=True).str.strip()

        # Fetch coordinates and add as new columns
        df["lat"], df["long"] = zip(*df["Burgh_Cleaned"].apply(fetch_coordinates))

        # Append to the consolidated DataFrame
        consolidated_df = pd.concat([consolidated_df, df], ignore_index=True)

# Save the consolidated DataFrame to a single CSV
consolidated_df.to_csv(output_file, index=False)

print(f"Consolidated data saved to {output_file}")
