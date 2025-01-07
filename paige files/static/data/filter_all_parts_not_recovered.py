from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons']

# Query to find documents where 'detailsOfRecovery.allPartsRecovered' is false
query = {"detailsOfRecovery.allPartsRecovered": False}
documents = collection.find(query)

# Initialize the list for filtered data
filtered_data = []

# Print and collect the results
print("Documents with allPartsRecovered as False:")
for doc in documents:
    print(f"Case ID: {doc.get('_id')}, State: {doc.get('circumstances', {}).get('address', {}).get('state', {}).get('name')}, All Parts Recovered: {doc.get('detailsOfRecovery', {}).get('allPartsRecovered')}")
    filtered_data.append(doc)

# Check if filtered_data is empty
if not filtered_data:
    print("No documents found with 'detailsOfRecovery.allPartsRecovered' as False.")
else:
    # Optionally, you can save the filtered data to a new collection or file
    db['UnidentifiedPersons_AllPartsNotRecovered'].insert_many(filtered_data)
    print("Filtered data has been processed and saved.")

print("Script completed successfully.")
