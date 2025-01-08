import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons']

# County coordinates mapping
county_coordinates = {
    "Milwaukee County, Wisconsin": (43.0000, -87.9671),
    "Vilas County, Wisconsin": (46.0000, -89.5000),
    "Sweetwater County, Wyoming": (41.6000, -108.0000),
    "Teton County, Wyoming": (43.5000, -110.8000),
    "Carbon County, Wyoming": (41.6000, -106.5000),
    "Park County, Wyoming": (44.5000, -109.0000),
    "Laramie County, Wyoming": (41.3000, -104.5000),
    "Campbell County, Wyoming": (44.8000, -105.5000)
}

# Function to get coordinates for a county
def get_county_coordinates(state, county):
    county_key = f"{county}, {state}"
    return county_coordinates.get(county_key, None)

# Query all data from MongoDB collection
documents = collection.find({})

# Initialize a GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Convert MongoDB documents to GeoJSON features
for doc in documents:
    location_data = None
    if "publicGeolocation" in doc and "coordinates" in doc["publicGeolocation"]:
        location_data = {
            "coordinates": [
                doc["publicGeolocation"]["coordinates"].get("lon"),
                doc["publicGeolocation"]["coordinates"].get("lat")
            ]
        }
    elif "circumstances" in doc and "address" in doc["circumstances"]:
        address = doc["circumstances"]["address"]
        if "state" in address and "name" in address["state"] and "county" in address and "name" in address["county"]:
            county = address["county"]["name"]
            state = address["state"]["name"]
            coordinates = get_county_coordinates(state, county)
            if coordinates:
                location_data = {
                    "coordinates": [coordinates[1], coordinates[0]],
                    "city": address.get("city"),
                    "state": state,
                    "county": county
                }
    
    if location_data:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": location_data["coordinates"]
            },
            "properties": {
                "case_id": str(doc.get("_id")),
                "idFormatted": doc.get("idFormatted"),
                "createdDateTime": doc.get("publicationStatus", {}).get("createdDateTime"),
                "modifiedDateTime": doc.get("publicationStatus", {}).get("modifiedDateTime"),
                "date_found": doc.get("circumstances", {}).get("dateFound"),
                "description": doc.get("circumstances", {}).get("description"),
                "state": location_data.get("state"),
                "county": location_data.get("county"),
                "city": location_data.get("city")
            }
        }
        geojson["features"].append(feature)
    else:
        print(f"No location data for document ID: {doc.get('_id')}")

# Print the number of features added
print(f"Number of features added to GeoJSON: {len(geojson['features'])}")

# Save to a GeoJSON file
with open('unidentified_persons.geojson', 'w') as file:
    json.dump(geojson, file, indent=4)

print("GeoJSON file created successfully.")
