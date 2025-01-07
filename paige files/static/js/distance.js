import * as turf from '@turf/turf';

export function findClosestDistance(set1, set2) {
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
export function processGeoJSONFiles(geoJSON1, geoJSON2) {
  const featureCollection1 = turf.featureCollection(geoJSON1.features);
  const featureCollection2 = turf.featureCollection(geoJSON2.features);

  return findClosestDistance(featureCollection1, featureCollection2);
}

