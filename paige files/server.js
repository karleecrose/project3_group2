const express = require('express');
const { MongoClient } = require('mongodb');
const app = express();
const port = 3000;
const uri = 'mongodb://127.0.0.1:27017';
const client = new MongoClient(uri);

app.use(express.static('static'));

app.get('/api/caves', async (req, res) => {
    try {
        await client.connect();
        const database = client.db('myDatabase');
        const collection = database.collection('caves');
        const caves = await collection.find({}).toArray();
        res.json(caves);
    } catch (err) {
        res.status(500).send(err);
    } finally {
        await client.close();
    }
});

app.get('/api/unidentified', async (req, res) => {
    try {
        await client.connect();
        const database = client.db('myDatabase');
        const collection = database.collection('unidentified');
        const unidentified = await collection.find({}).toArray();
        res.json(unidentified);
    } catch (err) {
        res.status(500).send(err);
    } finally {
        await client.close();
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
