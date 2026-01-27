"use strict";

const svg = d3.select("svg");
const g = svg.append("g");
const width = +svg.attr("width");
const height = +svg.attr("height");

d3.json("./map_data/COUNTY_MOI_1140317.json").then((data) => {
  console.log(data);
  const testData = data.features[0];

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

  g.attr("transform", "translate(-500, 30) scale(1)");
});
