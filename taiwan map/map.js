"use strict";

const svg = d3.select(".svg__big");
const g = svg.append("g");
const width = +svg.attr("width");
const height = +svg.attr("height");

d3.json("./map_data/COUNTY_MOI_1140317.json").then((data) => {
  console.log(data);
  // const testData = data.features[0];
  data.features.splice(0, 1);
  data.features.splice(12, 1);

  const projection = d3
    .geoIdentity()
    .reflectY(true)
    .fitSize([width, height], data);

  const pathGenerator = d3.geoPath().projection(projection);

  g.selectAll("path")
    .data(data.features)
    .enter()
    .append("path")
    .attr("d", pathGenerator)
    .attr("class", "county")
    .append("title")
    .text((d) => d.properties.COUNTYNAME); // tooltip

  g.attr("transform", "translate(-600, 1) scale(1.2)");
});
