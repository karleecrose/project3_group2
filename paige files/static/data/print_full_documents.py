from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection_name = 'UnidentifiedPersons_AllPartsNotRecovered'
collection = db[collection_name]

# Query to find documents where 'detailsOfRecovery.allPartsRecovered' is false
query = {"detailsOfRecovery.allPartsRecovered": False}
documents = collection.find(query)

# Print the full document details
print("Printing full document details:")
for doc in documents:
    print(f"Full Document: {doc}")
    print("\n")

print("Total documents:", documents.count_documents(query))
