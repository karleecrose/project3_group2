import json
from bson import ObjectId

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

# Load the full details JSON file
with open('unidentified_persons_full_details.json', 'r') as file:
    data = json.load(file)

# Initialize the list for GeoJSON features
features = []

# Process each document and extract coordinates and details
for doc in data:
    coordinates = doc.get('circumstances', {}).get('publicGeolocation', {}).get('coordinates')
    case_id = str(doc.get('_id'))
    
    if coordinates:
        lat = coordinates.get('lat')
        lon = coordinates.get('lon')

        if lat is not None and lon is not None:
            # Create GeoJSON feature with coordinates
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]  # GeoJSON format: [longitude, latitude]
                },
                "properties": {
                    "case_id": case_id,
                    "state": doc.get('circumstances', {}).get('address', {}).get('state', {}).get('name'),
                    "city": doc.get('circumstances', {}).get('address', {}).get('city'),
                    "county": doc.get('circumstances', {}).get('address', {}).get('county', {}).get('name'),
                    "date_found": doc.get('circumstances', {}).get('dateFound'),
                    "found_on_tribal_land": doc.get('circumstances', {}).get('foundOnTribalLand', {}).get('name'),
                    "circumstances_of_recovery": doc.get('circumstances', {}).get('circumstancesOfRecovery'),
                    "status": doc.get('circumstances', {}).get('status', {}).get('name')
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
