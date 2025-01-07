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
    coordinates = doc.get('publicGeolocation', {}).get('coordinates')
    case_id = str(doc.get('_id'))
    
    print(f"Case ID: {case_id}")
    if coordinates:
        lat = coordinates.get('lat')
        lon = coordinates.get('lon')
        print(f"Coordinates: lat={lat}, lon={lon}")

        if lat is not None and lon is not None:
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
        else:
            print(f"Missing lat or lon for Case ID: {case_id}")
    else:
        print(f"Missing coordinates for Case ID: {case_id}")

# Create GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Save GeoJSON to file
with open('missing_people.geojson', 'w') as file:
    json.dump(geojson, file, indent=4, cls=JSONEncoder)

print("GeoJSON file 'missing_people.geojson' has been created with features:", len(features))
