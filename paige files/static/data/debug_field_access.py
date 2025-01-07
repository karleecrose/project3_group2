import json
from pymongo import MongoClient
from bson import ObjectId

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection_name = 'UnidentifiedPersons_AllPartsNotRecovered'
collection = db[collection_name]

# Query to find documents where 'detailsOfRecovery.allPartsRecovered' is false
query = {"detailsOfRecovery.allPartsRecovered": False}
documents = collection.find(query)

# Initialize the list for GeoJSON features
features = []

# Print and collect the results
print(f"Listing documents with allPartsRecovered as False in collection {collection_name}:")
for doc in documents:
    public_geolocation = doc.get('publicGeolocation')
    case_id = str(doc.get('_id'))
    
    print(f"Case ID: {case_id}")
    print(f"publicGeolocation Field: {public_geolocation}")  # Debugging line
    
    if public_geolocation:
        coordinates = public_geolocation.get('coordinates')
        if coordinates:
            try:
                lat = float(coordinates.get('lat'))
                lon = float(coordinates.get('lon'))
                print(f"Parsed Coordinates: lat={lat}, lon={lon}")

                # Create GeoJSON feature with coordinates
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": {
                        "case_id": case_id,
                        "state": doc.get('circumstances', {}).get('address', {}).get('state', {}).get('name')
                    }
                }
                features.append(feature)
            except (TypeError, ValueError) as e:
                print(f"Error parsing coordinates for Case ID: {case_id}: {e}")
        else:
            print(f"Missing coordinates for Case ID: {case_id}")
    else:
        print(f"Missing publicGeolocation for Case ID: {case_id}")

# Create GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Save GeoJSON to file
with open('missing_people.geojson', 'w') as file:
    json.dump(geojson, file, indent=4, cls=JSONEncoder)

print("GeoJSON file 'missing_people.geojson' has been created with features:", len(features))
