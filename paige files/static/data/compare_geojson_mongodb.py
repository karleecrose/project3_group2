import json
from pymongo import MongoClient
from deepdiff import DeepDiff  # Ensure this import is here

# Load JSON data from GeoJSON file
with open('unidentified.geojson', 'r') as file:
    geojson_data = json.load(file)

# Extract features from GeoJSON (assuming features contain your data)
geojson_features = geojson_data.get('features', [])

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons']

# Query all data from MongoDB collection
mongodb_data = list(collection.find({}))

# Compare the data
diff = DeepDiff(geojson_features, mongodb_data, ignore_order=True)
print("Differences between the GeoJSON file and MongoDB data:")
print(diff)
