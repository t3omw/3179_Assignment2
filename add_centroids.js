import fs from "fs";
import * as topojson from "topojson-client";
import * as d3 from "d3-geo";

const topo = JSON.parse(fs.readFileSync("malaysia_state.json", "utf8"));
const geo = topojson.feature(topo, topo.objects.malaysia_state);

// Add centroid [longitude, latitude] to each feature
geo.features.forEach(f => {
  const [lon, lat] = d3.geoCentroid(f);
  f.properties.centroid = [lon, lat];
});

fs.writeFileSync("malaysia_state_with_centroid.json", JSON.stringify(geo, null, 2));
console.log("✅ Done: malaysia_state_with_centroid.json written.");
