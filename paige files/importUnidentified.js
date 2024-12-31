const fs = require('fs');
const { MongoClient } = require('mongodb');

const uri = 'mongodb://127.0.0.1:27017';
const client = new MongoClient(uri);

async function run() {
    try {
        await client.connect();
        const database = client.db('myDatabase');
        const collection = database.collection('unidentified');

        // Update this path to where your unidentified.geojson file is located
        const data = fs.readFileSync('C:/Users/16154/vu/Group Project/project 3/paige files/static/data/unidentified.geojson', 'utf8');
        const geojson = JSON.parse(data);

        if (geojson.type === 'FeatureCollection') {
            await collection.insertMany(geojson.features);
            console.log('Data imported successfully');
        } else {
            console.error('Invalid GeoJSON format');
        }
    } catch (err) {
        console.error(err);
    } finally {
        await client.close();
    }
}

run();
