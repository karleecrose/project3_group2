import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons']

# Query all data from MongoDB collection
documents = collection.find({})

# Initialize a GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Convert MongoDB documents to GeoJSON features
for doc in documents:
    if "publicGeolocation" in doc:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [doc["publicGeolocation"]["coordinates"]["lon"], doc["publicGeolocation"]["coordinates"]["lat"]]
            },
            "properties": {
                "case_id": doc.get("_id"),
                "date_found": doc.get("circumstances", {}).get("dateFound"),
                "description": doc.get("circumstances", {}).get("description"),
                "state": doc.get("circumstances", {}).get("address", {}).get("state", {}).get("name"),
                "county": doc.get("circumstances", {}).get("address", {}).get("county", {}).get("name"),
                "city": doc.get("circumstances", {}).get("address", {}).get("city")
            }
        }
        geojson["features"].append(feature)

# Save to a GeoJSON file
with open('unidentified_persons.geojson', 'w') as file:
    json.dump(geojson, file, indent=4)

print("GeoJSON file created successfully.")
