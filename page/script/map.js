"use strict";

const svg = d3.select(".svg__big");
const g = svg.append("g");
const width = +svg.attr("width");
const height = +svg.attr("height");
const cityApiMap = {
  宜蘭縣: "/v1/rest/datastore/F-D0047-003",
  桃園市: "/v1/rest/datastore/F-D0047-007",
  新竹縣: "/v1/rest/datastore/F-D0047-011",
  苗栗縣: "/v1/rest/datastore/F-D0047-015",
  彰化縣: "/v1/rest/datastore/F-D0047-019",
  南投縣: "/v1/rest/datastore/F-D0047-023",
  雲林縣: "/v1/rest/datastore/F-D0047-027",
  嘉義縣: "/v1/rest/datastore/F-D0047-031",
  屏東縣: "/v1/rest/datastore/F-D0047-035",
  臺東縣: "/v1/rest/datastore/F-D0047-039",
  花蓮縣: "/v1/rest/datastore/F-D0047-043",
  澎湖縣: "/v1/rest/datastore/F-D0047-047",
  基隆市: "/v1/rest/datastore/F-D0047-051",
  新竹市: "/v1/rest/datastore/F-D0047-055",
  嘉義市: "/v1/rest/datastore/F-D0047-059",
  臺北市: "/v1/rest/datastore/F-D0047-063",
  高雄市: "/v1/rest/datastore/F-D0047-067",
  新北市: "/v1/rest/datastore/F-D0047-071",
  臺中市: "/v1/rest/datastore/F-D0047-075",
  臺南市: "/v1/rest/datastore/F-D0047-079",
  連江縣: "/v1/rest/datastore/F-D0047-083",
  金門縣: "/v1/rest/datastore/F-D0047-087",
};
const areaApiMap = {
  嘉義縣: 0,
  新北市: 1,
  嘉義市: 2,
  新竹縣: 3,
  新竹市: 4,
  臺北市: 5,
  臺南市: 6,
  宜蘭縣: 7,
  苗栗縣: 8,
  雲林縣: 9,
  花蓮縣: 10,
  臺中市: 11,
  臺東縣: 12,
  桃園市: 13,
  南投縣: 14,
  高雄市: 15,
  金門縣: 16,
  屏東縣: 17,
  基隆市: 18,
  澎湖縣: 19,
  彰化縣: 20,
  連江縣: 21,
};

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
      const url = "/v1/rest/datastore/F-C0032-001";

      const req = await fetch(url);

      const response = await req.json();
      console.log(response.data[areaApiMap[`${county}`]]);

      cityTitle.textContent = "";
      cityTitle.textContent = `${county}　天氣概況`;

      const btnText = document.getElementById("county-name");
      const weatherBtn = document.getElementById("weatherBtn");
      weatherBtn.addEventListener("click", () => {
        const cityName = cityTitle.textContent.slice(0, 3);
        btnText.textContent = cityName;
      });
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
    .append("title")
    .text((d) => d.properties.COUNTYNAME); // tooltip

  g2.attr("transform", "translate(-60, -385) scale(0.5)");
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
