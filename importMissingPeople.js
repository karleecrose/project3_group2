const fs = require('fs');
const { MongoClient } = require('mongodb');

async function main() {
    const uri = 'mongodb://127.0.0.1:27017';
    const client = new MongoClient(uri);

    try {
        await client.connect();
        const database = client.db('myDatabase');
        const collection = database.collection('missing_people');

        // Read GeoJSON data
        const data = JSON.parse(fs.readFileSync('missing_people.geojson', 'utf8'));

        // Insert GeoJSON data into MongoDB
        await collection.insertMany(data.features);
        console.log('Data successfully imported');
    } finally {
        await client.close();
    }
}

main().catch(console.error);
