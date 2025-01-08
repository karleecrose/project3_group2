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

# Initialize the list for results
results = []

# Collect the results
print(f"Listing documents with allPartsRecovered as False in collection {collection_name}:")
for doc in documents:
    results.append(doc)

# Save JSON to file
with open('unidentified_persons_full_details.json', 'w') as file:
    json.dump(results, file, indent=4, cls=JSONEncoder)

print("JSON file 'unidentified_persons_full_details.json' has been created with documents:", len(results))
