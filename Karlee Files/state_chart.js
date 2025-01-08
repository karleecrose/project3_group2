// Import Vega-Lite
import embed from 'vega-embed';

// Fetch the chart specification
fetch('state_chart.json')
  .then(response => response.json())
  .then(spec => {
    vegaEmbed('#chart-container', spec).catch(console.error);
  });