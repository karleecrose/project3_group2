import json

# Load the missing_people.geojson file
with open('missing_people.geojson', 'r') as file:
    data = json.load(file)

# Check the first feature to see if it has coordinates
if data['features']:
    first_feature = data['features'][0]
    coordinates = first_feature.get('geometry', {}).get('coordinates')
    
    if coordinates:
        print(f"Coordinates: {coordinates}")
    else:
        print("No coordinates found in the first feature.")
else:
    print("No features found in the GeoJSON file.")
