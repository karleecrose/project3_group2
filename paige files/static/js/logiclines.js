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
                        }).bindPopup(`
                            <h3>${feature.properties.name || 'No Name Available'}</h3>
                            <p>Entry Date: ${feature.properties.entry_date || 'No Entry Date Available'}</p>
                        `);
                    }
                }).addTo(caves);
                caves.addTo(map); // Ensure the caves layer is added to the map
            })
            .catch(error => console.log('Error fetching caves data:', error));

        // Define the layer for unidentified remains
        var unidentifiedRemains = L.layerGroup();

        // Fetch and add GeoJSON data for unidentified remains
        fetch('static/data/unidentified.geojson')
            .then(response => response.json())
            .then(data => {
                L.geoJson(data, {
                    pointToLayer: function (feature, latlng) {
                        return L.circleMarker(latlng, {
                            radius: 6,
                            fillColor: "#8B0000", // Blood red fill color
                            color: "#4B0000", // Dark red border color
                            weight: 1,
                            opacity: 1,
                            fillOpacity: 0.8
                        }).bindPopup(`
                            <h3>Case: ${feature.properties.case || 'No Case ID Available'}</h3>
                            <p><b>City:</b> ${feature.properties.city || 'No City Available'}</p>
                            <p><b>State:</b> ${feature.properties.state || 'No State Available'}</p>
                            <p><b>Age From:</b> ${feature.properties.age_from || 'N/A'}</p>
                            <p><b>Age To:</b> ${feature.properties.age_to || 'N/A'}</p>
                            <p><b>Biological Sex:</b> ${feature.properties.biological_sex || 'N/A'}</p>
                            <p><b>Race/Ethnicity:</b> ${feature.properties.race_ethnicity || 'N/A'}</p>
                            <p><b>Date Modified:</b> ${feature.properties.date_modified || 'No Date Available'}</p>
                            <img src="assets/rockin-through_1.jfif" alt="Cave Victim" style="width:100px;height:auto;">
                        `);
                    }
                }).addTo(unidentifiedRemains);
                unidentifiedRemains.addTo(map); // Ensure the unidentified remains layer is added to the map
            })
            .catch(error => console.log('Error fetching unidentified remains data:', error));

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

        var overlayMaps = {
            "Caves": caves,
            "Unidentified Remains": unidentifiedRemains,
            "Distance Lines": distanceLines // Add distance lines as an overlay option
        };

        // Add layer controls to the map
<<<<<<< HEAD
        L.control.layers(baseMaps, overlayMaps).addTo(map);

=======
        L.control.layers(baseMaps, overlayMaps).addTo(map);
>>>>>>> 5c3d4e1 (completed)
