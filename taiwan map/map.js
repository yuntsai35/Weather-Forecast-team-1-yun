"use strict";

const svg = d3.select(".svg__big");
const g = svg.append("g");
const width = +svg.attr("width");
const height = +svg.attr("height");

// 本島+澎湖
d3.json("./map_data/COUNTY_MOI_1140317.json").then((data) => {
  console.log(data);
  const testData = data.features[0];
  data.features.splice(0, 1);
  data.features.splice(12, 1);

  const projection = d3
    .geoIdentity()
    .reflectY(true)
    .fitSize([width, height], data);

  const pathGenerator = d3.geoPath().projection(projection);

  g.attr("class", "g__big");
  g.selectAll("path")
    .data(data.features)
    .enter()
    .append("path")
    .attr("d", pathGenerator)
    .attr("class", "county")
    .append("title")
    .text((d) => d.properties.COUNTYNAME); // tooltip

  g.attr("transform", "translate(-580, 1) scale(1.2)");
});

// 連江縣
const svg1 = d3.select(".svg__small--z");
const g1 = svg1.append("g");
const width1 = +svg1.attr("width");
const height1 = +svg1.attr("height");
d3.json("./map_data/COUNTY_MOI_1140317.json").then((data) => {
  data.features.splice(1, 21);
  console.log(data);

  const projection = d3
    .geoIdentity()
    .reflectY(true)
    .fitSize([width1, height1], data);

  const pathGenerator = d3.geoPath().projection(projection);

  // const bounds = pathGenerator.bounds(data);
  // const scale = 50;
  // const dx = bounds[1][0] - bounds[0][0];
  // const dy = bounds[1][1] - bounds[0][1];
  // const x = (width1 - dx) / 2 - bounds[0][0];
  // const y = (height1 - dy) / 2 - bounds[0][1];
  // console.log(x, y);
  // g1.attr("transform", `translate(${x}, ${y}) scale(${scale})`);

  g1.selectAll("path")
    .data(data.features)
    .enter()
    .append("path")
    .attr("d", pathGenerator)
    .attr("class", "country")
    .append("title")
    .text((d) => d.properties.COUNTYNAME); // tooltip

  g1.attr("transform", "translate(20, -300) scale(0.5)");
});
// 20-300
// 金門縣
const svg2 = d3.select(".svg__small--c");
const g2 = svg2.append("g");
const width2 = +svg2.attr("width");
const height2 = +svg2.attr("height");
d3.json("./map_data/COUNTY_MOI_1140317.json").then((data) => {
  data.features.splice(0, 13);
  data.features.splice(1, 8);
  // console.log(data.features);

  const projection = d3
    .geoIdentity()
    .reflectY(true)
    .fitSize([width2, height2], data);

  const pathGenerator = d3.geoPath().projection(projection);

  g2.selectAll("path")
    .data(data.features)
    .enter()
    .append("path")
    .attr("d", pathGenerator)
    .attr("class", "country2")
    .append("title")
    .text((d) => d.properties.COUNTYNAME); // tooltip

  g2.attr("transform", "translate(-60, -385) scale(0.5)");
});
