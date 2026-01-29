import { initChart } from "./chart.js";

const countyApiMap = {
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

let currentTownData = [];
let currentSelectedCounty = "";
let currentSelectedTown = "";
let allRainfallData = null;

export function initDataSection() {
  renderCountyDropdown();

  // 初始化按鈕狀態為禁用
  const weeklyBtn = document.querySelector("#weekly-btn");
  const rainfallBtn = document.querySelector("#rainfall-btn");
  const discordBtn = document.querySelector("#discord-btn");

  if (weeklyBtn) weeklyBtn.disabled = true;
  if (rainfallBtn) rainfallBtn.disabled = true;
  if (discordBtn) discordBtn.classList.add("is-hidden");

  // 點擊外部區域自動收合下拉選單
  document.addEventListener("click", function (e) {
    const countyBtn = document.querySelector("#county-btn");
    const countyOptions = document.getElementById("county-options");
    const areaBtn = document.querySelector("#area-btn");
    const areaOptions = document.getElementById("area-options");

    // 檢查點擊是否在縣市下拉選單外部
    if (countyBtn && countyOptions) {
      const isClickInsideCounty =
        countyBtn.contains(e.target) || countyOptions.contains(e.target);
      if (!isClickInsideCounty) {
        countyOptions.classList.remove("is-open");
      }
    }

    // 檢查點擊是否在鄉鎮下拉選單外部
    if (areaBtn && areaOptions) {
      const isClickInsideArea =
        areaBtn.contains(e.target) || areaOptions.contains(e.target);
      if (!isClickInsideArea) {
        areaOptions.classList.remove("is-open");
      }
    }
  });

  const weatherBtn = document.querySelector("#weatherBtn");
  if (weatherBtn) {
    weatherBtn.addEventListener("click", function () {
      const countyTitle = document.querySelector(".cityTitle");

      if (countyTitle && countyTitle.textContent) {
        // 只取縣市名稱
        const fullText = countyTitle.textContent.trim();
        const selectedCounty = fullText.split(/\s+/)[0]; // 用空白分割，取第一個

        // 檢查該縣市是否存在於 countyApiMap
        if (countyApiMap[selectedCounty]) {
          console.log("找到對應的縣市，準備選擇..."); // 確認有找到縣市

          // 自動選擇該縣市
          selectCounty(selectedCounty);

          // 延遲滾動
          setTimeout(() => {
            const dataSection = document.querySelector(".data-section");
            if (dataSection) {
              const rect = dataSection.getBoundingClientRect();
              const scrollTop =
                window.pageYOffset || document.documentElement.scrollTop;
              const targetPosition = rect.top + scrollTop;

              window.scrollTo({
                top: targetPosition,
                behavior: "smooth",
              });
            }
          }, 150);
        } else {
          console.warn(`找不到對應的縣市：${selectedCounty}`);
        }
      }
    });
  }

  const countyBtn = document.querySelector("#county-btn");
  const countyOptions = document.getElementById("county-options");
  if (countyBtn) {
    countyBtn.addEventListener("click", function () {
      countyOptions.classList.toggle("is-open");
    });
  }

  const areaBtn = document.querySelector("#area-btn");
  const areaOptions = document.getElementById("area-options");
  if (areaBtn) {
    areaBtn.addEventListener("click", function () {
      areaOptions.classList.toggle("is-open");
    });
  }

  if (weeklyBtn) {
    weeklyBtn.addEventListener("click", function () {
      if (!weeklyBtn.disabled) {
        switchButton("weekly");
      }
    });
  }

  if (rainfallBtn) {
    rainfallBtn.addEventListener("click", function () {
      if (!rainfallBtn.disabled) {
        switchButton("rainfall");
      }
    });
  }

  function switchButton(button) {
    const weatherWrap = document.querySelector(".weather-wrap");
    const rainfallDataWrap = document.querySelector(".rainfall-data-wrap");
    const areaBtn = document.querySelector("#area-btn");
    const discordBtn = document.querySelector("#discord-btn");

    if (button === "weekly") {
      weeklyBtn.classList.add("active");
      rainfallBtn.classList.remove("active");
      areaBtn.classList.remove("is-hidden");
      discordBtn.classList.remove("is-hidden");

      weatherWrap.hidden = false;
      rainfallDataWrap.hidden = true;
    } else {
      weeklyBtn.classList.remove("active");
      rainfallBtn.classList.add("active");
      areaBtn.classList.add("is-hidden");
      discordBtn.classList.add("is-hidden");

      weatherWrap.hidden = true;
      rainfallDataWrap.hidden = false;

      // 切換到雨量觀測時，如果以選擇縣市，載入雨量資料
      if (currentSelectedCounty) {
        getRainfallData(currentSelectedCounty);
      }
    }
  }
}

// ===== Dropdown =====

function renderCountyDropdown() {
  const countyOptions = document.getElementById("county-options");
  countyOptions.innerHTML = "";

  Object.keys(countyApiMap).forEach(function (countyName) {
    const li = createOption(countyName);
    li.addEventListener("click", function () {
      selectCounty(countyName);
    });
    countyOptions.appendChild(li);
  });
}

function selectCounty(countyName) {
  const countyOptions = document.getElementById("county-options");
  const areaOptions = document.getElementById("area-options");
  const weatherWrap = document.querySelector(".weather-wrap");
  const rainfallDataWrap = document.querySelector(".rainfall-data-wrap");
  const weeklyBtn = document.querySelector("#weekly-btn");
  const rainfallBtn = document.querySelector("#rainfall-btn");
  const discordBtn = document.querySelector("#discord-btn");

  currentSelectedCounty = countyName;
  currentSelectedTown = ""; // 重設選擇

  // 啟動按鈕
  if (weeklyBtn) weeklyBtn.disabled = false;
  if (rainfallBtn) rainfallBtn.disabled = false;

  if (currentSelectedCounty) {
    const emptyContent = document.querySelector(".empty-content");
    emptyContent.classList.add("is-hidden");
  }

  if (currentSelectedTown === "") {
    const dateGroup = document.querySelector(".date-group");
    dateGroup.innerHTML = `<div class="date-group--empty">請選擇鄉鎮市區以查詢詳細天氣資訊</div>`;
  }

  document.querySelector("#county-btn .dropdown__text").textContent =
    countyName;
  countyOptions.classList.remove("is-open");

  // 檢查當前是哪個模式
  const isRainFallMode =
    rainfallBtn && rainfallBtn.classList.contains("active");

  if (isRainFallMode) {
    // 雨量觀測模式：只顯示雨量資料
    weatherWrap.hidden = true;
    rainfallDataWrap.hidden = false;
    getRainfallData(countyName);
  } else {
    // 一週天氣模式：顯示天氣資料
    weatherWrap.hidden = false;
    rainfallDataWrap.hidden = true;
    weeklyBtn.classList.add("active");
    discordBtn.classList.remove("is-hidden");
  }

  document.querySelector("#area-btn .dropdown__text").textContent =
    "選擇鄉鎮市區";
  areaOptions.innerHTML = "";

  const apiUrl = countyApiMap[countyName];
  getTownData(apiUrl);

  // 如果當前在雨量頁面，也更新雨量資料
  if (rainfallBtn && rainfallBtn.classList.contains("active")) {
    getRainfallData(countyName);
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

    // 選擇縣市後，自動載入第一個鄉鎮的圖表
    if (currentTownData.length > 0) {
      const firstTown = currentTownData[0];
      currentSelectedTown = firstTown.LocationName;
      initChart(firstTown.Time, firstTown.LocationName, currentSelectedCounty);
    }
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

      currentSelectedTown = item.LocationName;

      document.querySelector("#area-btn .dropdown__text").textContent =
        item.LocationName;
      areaOptions.classList.remove("is-open");

      // 更新表格
      renderWeeklyTable(item.Time);

      // 更新圖表
      initChart(item.Time, item.LocationName, currentSelectedCounty);

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

export async function getRainfallData(countyName) {
  try {
    if (!allRainfallData) {
      const apiUrl = `/v1/rest/datastore/O-A0002-001`;
      const res = await fetch(apiUrl);

      if (!res.ok) {
        throw new Error(`HTTP 錯誤： ${res.status}`);
      }

      const result = await res.json();

      if (result.success && result.data) {
        allRainfallData = result.data;
      } else {
        console.warn("無法取得雨量資料");
        clearRainfallTable();
        return;
      }
    }

    const countyStations = allRainfallData.filter(function (station) {
      return (
        station.CountyName === countyName ||
        station.CountyName === countyName.replace("臺", "台")
      );
    });

    if (countyStations.length > 0) {
      renderRainfallTable(countyStations);
    } else {
      console.warn(`找不到${countyName} 的測站資料`);

      result.data.slice(0, 5).forEach(function (station) {
        console.log("-", station.CountyName, station.StationName);
      });
      clearRainfallTable();
    }
  } catch (err) {
    console.error("取得雨量資料失敗", err);
    clearRainfallTable();
  }
}

function clearRainfallTable() {
  const rainfallDataGroup = document.querySelector(
    ".rainfall-data-wrap .area-group"
  );

  if (rainfallDataGroup) {
    rainfallDataGroup.innerHTML = "";
  }
}

function renderRainfallTable(rainfallData) {
  clearRainfallTable();

  const rainfallDataGroup = document.querySelector(
    ".rainfall-data-wrap .area-group"
  );

  if (!rainfallDataGroup) {
    console.error("找不到 rainfallDataGroup 元素");
    return;
  }

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
