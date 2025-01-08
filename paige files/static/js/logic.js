document.addEventListener('DOMContentLoaded', function () {
            // Initialize the map
            var map = L.map('map').setView([37.8, -96.9], 5); // Center of the US

        // Define base map with a dark theme
        var darkMap = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://carto.com/">CARTO</a>'
        }).addTo(map);
    // Define base map with a dark theme
    var darkMap = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>'
    }).addTo(map);

    // Define the Appalachian states
    const appalachianStates = [
        "Alabama", "Georgia", "Kentucky", "Maryland", "Mississippi", 
        "New York", "North Carolina", "Ohio", "Pennsylvania", 
        "South Carolina", "Tennessee", "Virginia", "West Virginia"
    ];

    // Function to filter features by Appalachian states
    function filterByAppalachianStates(feature) {
        return appalachianStates.includes(feature.properties.state);
    }

    // Define the layer for missing people
    var missingPeople = L.layerGroup();

    // Fetch and add GeoJSON data for missing people
    fetch('static/data/missing_people.geojson')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            L.geoJson(data, {
                filter: filterByAppalachianStates,
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, {
                        radius: 6,
                        fillColor: "#FFD700",
                        color: "#FF8C00",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).bindPopup(`
                        <strong>Case ID:</strong> ${feature.properties.case_id}<br>
                        <strong>Status:</strong> ${feature.properties.status}<br>
                        <strong>State:</strong> ${feature.properties.state}<br>
                        <strong>City:</strong> ${feature.properties.city}<br>
                        <strong>County:</strong> ${feature.properties.county}<br>
                        <strong>Date Found:</strong> ${feature.properties.date_found}<br>
                        <strong>Found on Tribal Land:</strong> ${feature.properties.found_on_tribal_land}<br>
                        <strong>Circumstances of Recovery:</strong> ${feature.properties.circumstances_of_recovery}
                    `);
                }
            }).addTo(missingPeople);
            missingPeople.addTo(map);
        })
        .catch(error => console.log('Error fetching missing people data:', error));

    // Define the layer for unidentified persons from NamUs scrape
    var namusScrape = L.layerGroup();

    // Fetch and add GeoJSON data for unidentified persons from NamUs scrape
    fetch('static/data/unidentified_persons.geojson')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            L.geoJson(data, {
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, {
                        radius: 6,
                        fillColor: "#FFFFFF",
                        color: "#FFFFFF",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).bindPopup(`
                        <strong>Case ID:</strong> ${feature.properties.case_id}<br>
                        <strong>State:</strong> ${feature.properties.state}
                    `);
                }
            }).addTo(namusScrape);
            namusScrape.addTo(map);
        })
        .catch(error => console.log('Error fetching unidentified persons data:', error));

    // Define the layer for unidentified persons
    var unidentified = L.layerGroup();

    // Fetch and add GeoJSON data for unidentified persons
    fetch('static/data/unidentified.geojson')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            L.geoJson(data, {
                filter: filterByAppalachianStates,
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, {
                        radius: 6,
                        fillColor: "#8B0000",
                        color: "#8B0000",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).bindPopup(`
                        <strong>Case ID:</strong> ${feature.properties.case_id}<br>
                        <strong>State:</strong> ${feature.properties.state}
                    `);
                }
            }).addTo(unidentified);
            unidentified.addTo(map);
        })
        .catch(error => console.log('Error fetching unidentified persons data:', error));

    // Define the layer for caves
    var caves = L.layerGroup();

    // Fetch and add GeoJSON data for caves
    fetch('static/data/caves.geojson')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            L.geoJson(data, {
                filter: filterByAppalachianStates,
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, {
                        radius: 6,
                        fillColor: "#FFA500",
                        color: "#FFA500",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).bindPopup(`
                        <strong>Cave Name:</strong> ${feature.properties.name || 'No Name Available'}<br>
                        <strong>State:</strong> ${feature.properties.state || 'No State Available'}
                    `);
                }
            }).addTo(caves);
            caves.addTo(map);
        })
        .catch(error => console.log('Error fetching caves data:', error));

    // Create a rivers layer
    var rivers = L.layerGroup();

    // USGS National Map API URL for hydrography (rivers and streams)
    let url = "https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/1/query?where=1%3D1&outFields=*&f=geojson";

    // Fetching and adding GeoJSON data for rivers
    fetch(url)
    .then(response => response.json())
    .then(data => {
        if (data && data.features) {
            L.geoJson(data, {
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, {
                        radius: 6,
                        fillColor: "#00BFFF",
                        color: "#1E90FF",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).bindPopup(`
                        <strong>River:</strong> ${feature.properties.GNIS_NAME || 'Unknown'}<br>
                        <strong>Feature ID:</strong> ${feature.properties.FEATUREID}
                    `);
                }
            }).addTo(rivers);
            rivers.addTo(map);
        } else {
            console.error("Data format is not correct:", data);
        }
    })
    .catch(error => console.error("Error fetching data:", error));

        // Define the layer for distance lines
        var distanceLines = L.layerGroup();

        // Function to load GeoJSON data from a file
        async function loadGeoJSON(url) {
            const response = await fetch(url);
            return await response.json();
        }

        // Function to find the shortest distance for each point in geojson2 to points in geojson1
        async function findClosestDistances() {
            const geojson1 = await loadGeoJSON('static/data/caves.geojson');
            const geojson2 = await loadGeoJSON('static/data/unidentified.geojson');

            const closestDistances = geojson2.features.map(feature2 => {
                let closestDistance = Infinity;
                let closestPoint = null;

                geojson1.features.forEach(feature1 => {
                    const point1 = turf.point(feature1.geometry.coordinates);
                    const point2 = turf.point(feature2.geometry.coordinates);
                    const distance = turf.distance(point1, point2, { units: 'miles' });

                    if (distance < closestDistance) {
                        closestDistance = distance;
                        closestPoint = feature1;
                    }
                });

                return {
                    point1: closestPoint,
                    point2: feature2,
                    distance: closestDistance
                };
            });

            return closestDistances;
        }

        // Function to initialize the map and display closest distances
        async function initializeMap() {
            const closestDistances = await findClosestDistances();

            // Add base map and layers
            darkMap.addTo(map);
            caves.addTo(map);
            unidentifiedRemains.addTo(map);
            distanceLines.addTo(map);

            // Display closest distances
            closestDistances.forEach(({ point1, point2, distance }) => {
                const marker1 = L.marker(point1.geometry.coordinates.reverse()).addTo(map);
                const marker2 = L.marker(point2.geometry.coordinates.reverse()).addTo(map);

                marker1.bindPopup(`Closest Distance to Unidentified Point: ${distance.toFixed(2)} miles`);
                marker2.bindPopup(`Closest Distance to Cave Point: ${distance.toFixed(2)} miles`);

                const line = L.polyline([
                    point1.geometry.coordinates,
                    point2.geometry.coordinates
                ], { color: 'gray' }).addTo(map);
            });
        }

        // Load and display closest distances on the map
        initializeMap();

        // Define base maps and overlay maps
        var baseMaps = {
            "Dark Map": darkMap
        };
    // Define base maps and overlay maps
    var baseMaps = {
        "Dark Map": darkMap
    };

    var overlayMaps = {
        "Missing People": missingPeople,
        "NamUs Scrape": namusScrape,
        "Unidentified Persons": unidentified,
        "Distance Lines": distanceLines // Add distance lines as an overlay option
        "Caves": caves,
        "Rivers": rivers
    };

        // Add layer controls to the map
        L.control.layers(baseMaps, overlayMaps).addTo(map);

    // Add layer controls to the map
    L.control.layers(baseMaps, overlayMaps).addTo(map);
});
