"use strict";

const svg = d3.select("svg");
const g = svg.append("g");
const width = +svg.attr("width");
const height = +svg.attr("height");

d3.json("./map_data/COUNTY_MOI_1140319.json").then((data) => {
  console.log(data);
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
});
