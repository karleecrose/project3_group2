from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons_AllPartsNotRecovered']

# Print details of all documents
print("Listing all documents in the collection:")
documents = collection.find()

for doc in documents:
    print(f"Case ID: {doc.get('_id')}")
    print(f"detailsOfRecovery.allPartsRecovered: {doc.get('detailsOfRecovery', {}).get('allPartsRecovered')}")
    print(f"publicGeolocation.coordinates: {doc.get('publicGeolocation', {}).get('coordinates')}")
    print("\n")

print("Total documents:", collection.count_documents({}))
