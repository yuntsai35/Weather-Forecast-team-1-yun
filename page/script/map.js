"use strict";

const svg = d3.select(".svg__big");
const g = svg.append("g");
const width = +svg.attr("width");
const height = +svg.attr("height");
let temparature = document.querySelector(".temparature");
let weatherStatus = document.querySelector(".status");
let weatherIcon = document.getElementById("icon");
const render = async function () {
  const urlOrigin = "/v1/rest/datastore/F-C0032-001?locationName=臺北市";
  const req = await fetch(urlOrigin);

  const response = await req.json();
  const data = response.data;
  temparature.textContent = `${data[0].MinT}℃ -${data[0].MaxT}℃ `;
  weatherStatus.textContent = `${data[0].Wx}`;
  if (data[0].Wx.includes("雲")) {
    weatherIcon.textContent = "cloud";
  }
  if (data[0].Wx.includes("雨")) {
    weatherIcon.textContent = "rainy";
  }
};
render();

// 本島+澎湖
d3.json("/page/map_data/COUNTY_MOI_1140317.json").then((data) => {
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
    .attr("data-county", (d) => d.properties.COUNTYNAME)
    .append("title")
    .text((d) => d.properties.COUNTYNAME); // tooltip

  g.attr("transform", "translate(-980, 100) scale(1.5)");

  // 獲取API
  const cities = document.querySelectorAll("path.county");
  const cityTitle = document.querySelector(".cityTitle");
  cities.forEach((path) => {
    path.addEventListener("click", async () => {
      const county = path.dataset.county;
      const url = `/v1/rest/datastore/F-C0032-001?locationName=${county}`;

      const req = await fetch(url);

      const response = await req.json();
      const data = response.data;
      console.log(data);

      cityTitle.textContent = "";
      cityTitle.textContent = `${county} 天氣概況`;

      temparature.textContent = `${data[0].MinT}℃ -${data[0].MaxT}℃ `;
      weatherStatus.textContent = `${data[0].Wx}`;
      weatherIcon.textContent = "cloud";
    });
  });
});

// 連江縣
const svg1 = d3.select(".svg__small--z");
const g1 = svg1.append("g");
const width1 = +svg1.attr("width");
const height1 = +svg1.attr("height");
d3.json("/page/map_data/COUNTY_MOI_1140317.json").then((data) => {
  data.features.splice(1, 21);

  const projection = d3
    .geoIdentity()
    .reflectY(true)
    .fitSize([width1, height1], data);

  const pathGenerator = d3.geoPath().projection(projection);

  g1.selectAll("path")
    .data(data.features)
    .enter()
    .append("path")
    .attr("d", pathGenerator)
    .attr("class", "country")
    .attr("data-id", (d) => d.properties.COUNTYID)
    .attr("data-county", (d) => d.properties.COUNTYNAME)
    .append("title")
    .text((d) => d.properties.COUNTYNAME); // tooltip

  g1.attr("transform", "translate(20, -300) scale(0.5)");

  // 獲取API
  const island1 = document.querySelector(".country");
  const cityTitle = document.querySelector(".cityTitle");
  island1.addEventListener("click", async () => {
    const county = island1.dataset.county;
    const url = `/v1/rest/datastore/F-C0032-001?locationName=${county}`;

    const req = await fetch(url);
    const response = await req.json();
    const data = response.data;
    console.log(data);

    cityTitle.textContent = "";
    cityTitle.textContent = `${county} 天氣概況`;

    temparature.textContent = `${data[0].MinT}℃ -${data[0].MaxT}℃ `;
    weatherStatus.textContent = `${data[0].Wx}`;
  });
});
// 20-300
// 金門縣
const svg2 = d3.select(".svg__small--c");
const g2 = svg2.append("g");
const width2 = +svg2.attr("width");
const height2 = +svg2.attr("height");
d3.json("/page/map_data/COUNTY_MOI_1140317.json").then((data) => {
  data.features.splice(0, 13);
  data.features.splice(1, 8);

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
    .attr("data-id", (d) => d.properties.COUNTYID)
    .attr("data-county", (d) => d.properties.COUNTYNAME)
    .append("title")
    .text((d) => d.properties.COUNTYNAME); // tooltip

  g2.attr("transform", "translate(-60, -385) scale(0.5)");

  // 獲取API
  const island2 = document.querySelector(".country2");
  const cityTitle = document.querySelector(".cityTitle");
  island2.addEventListener("click", async () => {
    const county = island2.dataset.county;
    const url = `/v1/rest/datastore/F-C0032-001?locationName=${county}`;

    const req = await fetch(url);
    const response = await req.json();
    const data = response.data;
    console.log(data);

    cityTitle.textContent = "";
    cityTitle.textContent = `${county} 天氣概況`;

    temparature.textContent = `${data[0].MinT}℃ -${data[0].MaxT}℃ `;
    weatherStatus.textContent = `${data[0].Wx}`;
  });
});

// svg 定位
// const bounds = pathGenerator.bounds(data);
// const scale = 50;
// const dx = bounds[1][0] - bounds[0][0];
// const dy = bounds[1][1] - bounds[0][1];
// const x = (width1 - dx) / 2 - bounds[0][0];
// const y = (height1 - dy) / 2 - bounds[0][1];
// console.log(x, y);
// g1.attr("transform", `translate(${x}, ${y}) scale(${scale})`);
