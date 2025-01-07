from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons_AllPartsNotRecovered']

# Query to find documents where 'detailsOfRecovery.allPartsRecovered' is false
query = {"detailsOfRecovery.allPartsRecovered": False}
documents = collection.find(query)

# Initialize a counter
total_documents = 0

# Print the details of all documents
print("Listing all documents with allPartsRecovered as False in the collection:")
for doc in documents:
    total_documents += 1
    print(f"Case ID: {doc.get('_id')}")
    print(f"detailsOfRecovery.allPartsRecovered: {doc.get('detailsOfRecovery', {}).get('allPartsRecovered')}")
    coordinates = doc.get('publicGeolocation', {}).get('coordinates')
    if coordinates:
        print(f"publicGeolocation.coordinates: {coordinates}")
    else:
        print("publicGeolocation.coordinates: None")
    print("\n")

print("Total documents:", total_documents)
