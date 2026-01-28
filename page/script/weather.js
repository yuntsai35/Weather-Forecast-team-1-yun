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
    }
  }
}

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

  document.querySelector("#city-btn .dropdown__text").textContent = cityName;
  cityOptions.classList.remove("is-open");

  document.querySelector("#area-btn .dropdown__text").textContent =
    "選擇鄉鎮市區";
  areaOptions.innerHTML = "";

  const apiUrl = cityApiMap[cityName];
  getTownData(apiUrl);
}

export async function getTownData(apiUrl) {
  try {
    const res = await fetch(apiUrl);

    if (!res.ok) {
      throw new Error(`HTTP 錯誤： ${res.status}`);
    }
    const result = await res.json();
    renderAreaDropdown(result.data);
  } catch (err) {
    console.error("取得鄉鎮市區資料失敗", err);
  }
}

function renderAreaDropdown(townData) {
  const areaOptions = document.getElementById("area-options");
  areaOptions.innerHTML = "";

  townData.forEach(function (item) {
    const li = createOption(item.LocationName);

    li.addEventListener("click", function (e) {
      e.stopPropagation();

      document.querySelector("#area-btn .dropdown__text").textContent =
        item.LocationName;

      areaOptions.classList.remove("is-open");
    });
    areaOptions.appendChild(li);
  });
}

function createOption(text) {
  const li = document.createElement("li");
  li.textContent = text;
  return li;
}
