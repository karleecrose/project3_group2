// Initialize the map
var map = L.map('map').setView([37.7749, -82.6381], 5);

// Define base map with a dark theme
var darkMap = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://carto.com/">CARTO</a>'
}).addTo(map);

// Define the layer for caves
var caves = L.layerGroup();

// Fetch and add GeoJSON data for caves
fetch('static/data/caves.geojson')
  .then(response => response.json())
  .then(data => {
    L.geoJson(data, {
      pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, {
          radius: 5,
          fillColor: "#ff7800",
          color: "#000",
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8
        }).bindPopup(`<h3>${feature.properties.name}</h3><p>${feature.properties.description}</p>`);
      }
    }).addTo(caves);
    caves.addTo(map); // Ensure the caves layer is added to the map
  })
  .catch(error => console.log('Error fetching caves data:', error));

// Define base maps and overlay maps
var baseMaps = {
  "Dark Map": darkMap
};

var overlayMaps = {
  "Caves": caves
};

// Add layer controls to the map
L.control.layers(baseMaps, overlayMaps).addTo(map);
