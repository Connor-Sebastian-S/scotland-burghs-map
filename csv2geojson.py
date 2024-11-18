import pandas as pd
import json

# Input and output file paths
csv_file = "./Updated_List_of_burghs_with_lat_long.csv"
json_file = "./burghs_data.json"

# Read the CSV
df = pd.read_csv(csv_file)

# Replace NaN or empty values with empty strings
df = df.fillna("")

# Convert to GeoJSON (Leaflet-friendly format)
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for _, row in df.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["long"], row["lat"]]
        },
        "properties": row.to_dict()  # Include all row data as properties
    }
    geojson_data["features"].append(feature)

# Save to JSON file
with open(json_file, "w") as f:
    json.dump(geojson_data, f)

print(f"GeoJSON data saved to {json_file}")
