const fs = require('fs');
const turf = require('@turf/turf');

// Function to read a GeoJSON file
function readGeoJSONFile(filePath) {
  const data = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(data);
}

// Read and parse your GeoJSON files
const set1 = readGeoJSONFile('static/data/caves.geojson');
const set2 = readGeoJSONFile('static/data/unidentified.geojson');

// Ensure the data is in the correct format for turf.js
const featureCollection1 = turf.featureCollection(set1.features);
const featureCollection2 = turf.featureCollection(set2.features);

// Function to calculate the closest distance between two sets of coordinates
function findClosestDistance(set1, set2) {
  let closestDistance = Infinity;
  let closestPoints = {};

  set1.features.forEach(point1 => {
    set2.features.forEach(point2 => {
      const distance = turf.distance(point1, point2);
      if (distance < closestDistance) {
        closestDistance = distance;
        closestPoints = { point1, point2 };
      }
    });
  });

  return { closestDistance, closestPoints };
}

// Find the closest distance between the two sets
const result = findClosestDistance(featureCollection1, featureCollection2);
console.log(`Closest Distance: ${result.closestDistance} kilometers`);
console.log(`Closest Points: ${JSON.stringify(result.closestPoints, null, 2)}`);
