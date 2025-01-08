from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['unidentifiedpersons_allpartsnotrecovered']  # Use the correct collection

# Query to find all documents
documents = collection.find()

# Print the details of all documents
print("Listing all documents in the collection:")
for doc in documents:
    print(f"Case ID: {doc.get('_id')}")
    for key, value in doc.items():
        print(f"{key}: {value}")
    print("\n")

print("Total documents:", collection.count_documents({}))
