import { processGeoJSONFiles } from './distance.js';

const geoJSON1 = readGeoJSONfile('./static/data/caves.geojson');
const geoJSON2 = readGeoJSONfile('./static/data/unidentified.geojson');

const result = processGeoJSONFiles(geoJSON1, geoJSON2);
console.log('Closest Distance: ${result.closestDistance} kilometers');
console.log('Closest Points: ${JSON.stringify(result.closestPoints, null, 2)}');