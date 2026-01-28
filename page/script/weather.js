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

// 縣市對應測站ID (主要測站)
const cityStationMap = {
  宜蘭縣: "C0X190",
  桃園市: "C0C480",
  新竹縣: "C0H990",
  苗栗縣: "C0K430",
  彰化縣: "C0M500",
  南投縣: "C0M610",
  雲林縣: "C0N310",
  嘉義縣: "C0R190",
  屏東縣: "C0S490",
  臺東縣: "C0T9A0",
  花蓮縣: "C0U750",
  澎湖縣: "C0Z050",
  基隆市: "C0A520",
  新竹市: "C0H930",
  嘉義市: "C0Q690",
  臺北市: "C0AC40",
  高雄市: "C0R800",
  新北市: "C0AD20",
  臺中市: "C0K150",
  臺南市: "C0R100",
  連江縣: "C0A9D0",
  金門縣: "C0X120",
};

let currentTownData = [];
let currentSelectedCity = "";

export function initDropdown() {
  renderCityDropdown();

  const cityBtn = document.querySelector("#city-btn");
  const cityOptions = document.getElementById("city-options");
  if (cityBtn) {
    cityBtn.addEventListener("click", function () {
      cityOptions.classList.toggle("is-open");
    });
  }

  const areaBtn = document.querySelector("#area-btn");
  const areaOptions = document.getElementById("area-options");
  if (areaBtn) {
    areaBtn.addEventListener("click", function () {
      areaOptions.classList.toggle("is-open");
    });
  }

  const weeklyBtn = document.querySelector("#weekly-btn");
  if (weeklyBtn) {
    weeklyBtn.addEventListener("click", function () {
      switchButton("weekly");
    });
  }

  const rainfallBtn = document.querySelector("#rainfall-btn");
  if (rainfallBtn) {
    rainfallBtn.addEventListener("click", function () {
      switchButton("rainfall");
    });
  }

  function switchButton(button) {
    const chartWrap = document.querySelector(".chart-wrap");
    const weeklyDataWrap = document.querySelector(".weekly-data-wrap");
    const rainfallDataWrap = document.querySelector(".rainfall-data-wrap");

    if (button === "weekly") {
      weeklyBtn.classList.add("active");
      rainfallBtn.classList.remove("active");

      chartWrap.hidden = false;
      weeklyDataWrap.hidden = false;
      rainfallDataWrap.hidden = true;
    } else {
      weeklyBtn.classList.remove("active");
      rainfallBtn.classList.add("active");

      chartWrap.hidden = true;
      weeklyDataWrap.hidden = true;
      rainfallDataWrap.hidden = false;

      // 切換到雨量觀測時，如果以選擇縣市，載入雨量資料
      if (currentSelectedCity) {
        getRainfallData(currentSelectedCity);
      }
    }
  }
}

// ===== Dropdown =====

function renderCityDropdown() {
  const cityOptions = document.getElementById("city-options");
  cityOptions.innerHTML = "";

  Object.keys(cityApiMap).forEach(function (cityName) {
    const li = createOption(cityName);
    li.addEventListener("click", function () {
      selectCity(cityName);
    });
    cityOptions.appendChild(li);
  });
}

function selectCity(cityName) {
  const cityOptions = document.getElementById("city-options");
  const areaOptions = document.getElementById("area-options");

  currentSelectedCity = cityName;

  document.querySelector("#city-btn .dropdown__text").textContent = cityName;
  cityOptions.classList.remove("is-open");

  document.querySelector("#area-btn .dropdown__text").textContent =
    "選擇鄉鎮市區";
  areaOptions.innerHTML = "";

  const apiUrl = cityApiMap[cityName];
  getTownData(apiUrl);

  // 如果當前在雨量頁面，也更新雨量資料
  const rainfallBtn = document.querySelector("#rainfall-btn");
  if (rainfallBtn && rainfallBtn.classList.contains("active")) {
    getRainfallData(cityName);
  }
}

export async function getTownData(apiUrl) {
  try {
    const res = await fetch(apiUrl);

    if (!res.ok) {
      throw new Error(`HTTP 錯誤： ${res.status}`);
    }
    const result = await res.json();
    currentTownData = result.data;
    renderAreaDropdown(currentTownData);
  } catch (err) {
    console.error("取得鄉鎮市區資料失敗", err);
  }
}

function renderAreaDropdown(townData) {
  const areaOptions = document.getElementById("area-options");
  const weeklyBtn = document.querySelector("#weekly-btn");
  areaOptions.innerHTML = "";

  townData.forEach(function (item) {
    const li = createOption(item.LocationName);

    li.addEventListener("click", function (e) {
      e.stopPropagation();

      document.querySelector("#area-btn .dropdown__text").textContent =
        item.LocationName;
      areaOptions.classList.remove("is-open");

      renderWeeklyTable(item.Time);
      weeklyBtn.classList.add("active");
    });
    areaOptions.appendChild(li);
  });
}

function createOption(text) {
  const li = document.createElement("li");
  li.textContent = text;
  return li;
}

// ===== Weekly Table =====

function clearWeeklyTable() {
  const dataGroup = document.querySelector(".date-group");
  dataGroup.innerHTML = "";
}

// Time 轉成 日期分組
function groupByDate(timeList) {
  const map = {};
  timeList.forEach(function (item) {
    const date = item.startTime.split("T")[0];
    if (!map[date]) {
      map[date] = [];
    }
    map[date].push(item);
  });
  return map;
}

function renderWeeklyTable(timeList) {
  clearWeeklyTable();

  const dateGroup = document.querySelector(".date-group");
  const groupedData = groupByDate(timeList);

  Object.keys(groupedData).forEach(function (date) {
    const table = document.createElement("table");
    table.className = "weekly-data-table";

    const tbody = document.createElement("tbody");
    table.appendChild(tbody);

    const dayData = groupedData[date];

    dayData.forEach(function (item, index) {
      const tr = document.createElement("tr");
      tr.className = "date-row";

      // 日期欄
      if (index === 0) {
        const tdDate = createDateCell(date, dayData.length);
        tr.appendChild(tdDate);
      }

      tr.appendChild(createIconCell(item.startTime));
      tr.appendChild(createTextCell(item.Weather));
      tr.appendChild(createTextCell(item.ProbabilityOfPrecipitation + "%"));
      tr.appendChild(createTextCell(item.Temperature + "°C"));
      tr.appendChild(createTextCell(item.RelativeHumidity + "%"));

      tbody.appendChild(tr);
    });
    dateGroup.appendChild(table);
  });
}

function createDateCell(date, rowspan) {
  const td = document.createElement("td");
  td.className = "date-cell";
  td.rowSpan = rowspan;

  const info = document.createElement("div");
  info.className = "date-info";

  const d = document.createElement("div");
  d.className = "date";
  d.textContent = formatDate(date);

  const w = document.createElement("div");
  w.className = "weekday";
  w.textContent = formatWeekday(date);

  info.appendChild(d);
  info.appendChild(w);
  td.appendChild(info);

  return td;
}

// 時間 icon
function createIconCell(startTime) {
  const td = document.createElement("td");
  td.className = "time-cell";

  const span = document.createElement("span");
  span.className = "material-symbols-outlined";

  const hour = parseInt(startTime.split("T")[1].split(":")[0]);

  span.textContent = hour >= 6 && hour < 18 ? "wb_sunny" : "bedtime";

  td.appendChild(span);
  return td;
}

// 文字欄
function createTextCell(text) {
  const td = document.createElement("td");
  td.textContent = text;
  return td;
}

function formatDate(dateStr) {
  const d = new Date(dateStr);
  return `${d.getMonth() + 1}/${d.getDate()}`;
}

function formatWeekday(dateStr) {
  const weeks = ["週日", "週一", "週二", "週三", "週四", "週五", "週六"];
  return weeks[new Date(dateStr).getDay()];
}

// ===== Rainfall Data =====

export async function getRainfallData(cityName) {
  const stationId = cityStationMap[cityName];

  if (!stationId) {
    console.error("找不到對應的測站");
    clearRainfallTable();
    return;
  }

  try {
    const res = await fetch(
      `/v1/rest/datastore/O-A0002-001?station_id=${stationId}`
    );

    if (!res.ok) {
      throw new Error(`HTTP 錯誤： ${res.status}`);
    }

    const result = await res.json();
    console.log(result.data);

    if (result.success && result.data && result.data.length > 0) {
      renderRainfallTable(result.data);
    } else {
      console.error("沒有雨量資料");
      clearRainfallTable();
    }
  } catch (err) {
    console.error("取得雨量資料失敗", err);
    clearRainfallTable();
  }
}

function clearRainfallTable() {
  const rainfallDataGroup = document.querySelector(
    ".rainfall-data-wrap .date-group"
  );

  if (rainfallDataGroup) {
    rainfallDataGroup.innerHTML = "";
  }
}

function renderRainfallTable(rainfallData) {
  clearRainfallTable();

  const rainfallDataGroup = document.querySelector(
    ".rainfall-data-wrap .date-group"
  );

  rainfallData.forEach(function (station) {
    const table = document.createElement("table");
    table.className = "rainfall-data-table";

    const tbody = document.createElement("tbody");

    const tr = document.createElement("tr");
    tr.className = "data-row";

    const tdStation = document.createElement("td");
    tdStation.textContent = station.StationName;
    tr.appendChild(tdStation);

    const tdNow = document.createElement("td");
    tdNow.textContent = formatRainfall(station.Now);
    tr.appendChild(tdNow);

    const td10Min = document.createElement("td");
    td10Min.textContent = formatRainfall(station.Past10Min);
    tr.appendChild(td10Min);

    const td1Hr = document.createElement("td");
    td1Hr.textContent = formatRainfall(station.Past1hr);
    tr.appendChild(td1Hr);

    const td3Hr = document.createElement("td");
    td3Hr.textContent = formatRainfall(station.Past3hr);
    tr.appendChild(td3Hr);

    const td6Hr = document.createElement("td");
    td6Hr.textContent = formatRainfall(station.Past6Hr);
    tr.appendChild(td6Hr);

    const td12Hr = document.createElement("td");
    td12Hr.textContent = formatRainfall(station.Past12hr);
    tr.appendChild(td12Hr);

    const td24Hr = document.createElement("td");
    td24Hr.textContent = formatRainfall(station.Past24hr);
    tr.appendChild(td24Hr);

    tbody.appendChild(tr);
    table.appendChild(tbody);
    rainfallDataGroup.appendChild(table);
  });
}

function formatRainfall(value) {
  // 處理無效值
  if (
    value === "-998" ||
    value === "-99" ||
    value === "T" ||
    !value ||
    value === "-998.00" ||
    value === "-99.00"
  ) {
    return "-";
  }

  // 轉為數字並格式化
  const num = parseFloat(value);
  if (isNaN(num)) {
    return "-";
  }

  return num.toFixed(1) + " mm";
}
