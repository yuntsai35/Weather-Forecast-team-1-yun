let temperatureChart = null;

/**
 * 初始化溫度曲線圖表
 * @param {Array} timeData - 時間資料陣列
 * @param {String} locationName - 地點名稱
 * @param {String} countyName - 縣市名稱
 */

export function initChart(timeData, locationName, countyName) {
  if (!Array.isArray(timeData) || timeData.length === 0) {
    console.warn("initChart：timeData 尚未準備好", timeData);
    return;
  }

  try {
    const temperatureData = processTemperatureData(timeData);

    const canvas = document.querySelector("#myChart");
    if (!canvas) {
      console.error("找不到 canvas 元素");
      return;
    }

    const ctx = canvas.getContext("2d");

    // 如果已存在圖表，先銷毀避免重複繪製
    if (temperatureChart) {
      temperatureChart.destroy(); // 載入後移除
    }

    temperatureChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: temperatureData.labels, // 日期
        datasets: [
          {
            label: "白天高溫",
            data: temperatureData.dayTemps,
            borderColor: "#FF6B35",
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            borderWidth: 3,
            tension: 0.4, // 曲線平滑度
            fill: true,
            pointRadius: 5,
            pointHoverRadius: 7,
            pointBackgroundColor: "#FF6B35",
            pointBorderColor: "#FFF",
            pointBorderWidth: 2,
          },
          {
            label: "晚上低溫",
            data: temperatureData.nightTemps,
            borderColor: "#4FC3F7",
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointRadius: 5,
            pointHoverRadius: 7,
            pointBackgroundColor: "#4FC3F7",
            pointBorderColor: "#FFF",
            pointBorderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false, // 允許自訂高度
        plugins: {
          legend: {
            display: true,
            position: "top",
            labels: {
              font: {
                size: 14,
                weight: "600",
              },
              padding: 15,
              usePointStyle: true,
            },
          },
          title: {
            display: true,
            text: `${countyName} ${locationName} - 溫度趨勢`,
            font: {
              size: 16,
              weight: "700",
            },
            padding: {
              top: 10,
              bottom: 20,
            },
          },
          tooltip: {
            mode: "index",
            intersect: false,
            callbacks: {
              label: function (context) {
                return context.dataset.label + ": " + context.parsed.y + "°C";
              },
            },
          },
        },
        scales: {
          y: {
            beginAtZero: false,
            ticks: {
              callback: function (value) {
                return value + "°C";
              },
            },
            title: {
              display: true,
              text: "溫度 (°C)",
            },
          },
          x: {
            title: {
              display: true,
              text: "日期",
            },
          },
        },
        interaction: {
          mode: "index",
          intersect: false,
        },
      },
    });
    console.log("圖表初始化完成：", countyName, locationName);
  } catch (err) {
    console.error("圖表初始化失敗：", err);
  }
}

/**
 * 處理溫度資料成圖表格式
 * @param {Array} timeData - 原始時間資料
 * @returns {Object} 處理後的資料 { labels, dayTemps, nightTemps }
 */

function processTemperatureData(timeData) {
  if (!Array.isArray(timeData)) {
    console.error("timeData 不是陣列：", timeData);
    return { labels: [], dayTemps: [], nightTemps: [] };
  }

  const labels = [];
  const dayTemps = [];
  const nightTemps = [];

  // 每 12 小時為一個時段，區分白天和晚上
  for (let i = 0; i < timeData.length; i += 2) {
    const dayData = timeData[i];
    const nightData = timeData[i + 1];

    if (dayData && nightData) {
      // 格式化日期
      const date = new Date(dayData.startTime);
      const dateStr = `${date.getMonth() + 1}/${date.getDate()}`;
      labels.push(dateStr);

      // 提取溫度數值
      const dayTemp = parseFloat(dayData.Temperature);
      const nightTemp = parseFloat(nightData.Temperature);

      // 判斷高低溫
      if (dayTemp >= nightTemp) {
        dayTemps.push(dayTemp);
        nightTemps.push(nightTemp);
      } else {
        dayTemps.push(nightTemp);
        nightTemps.push(dayTemp);
      }
    }
  }
  return { labels, dayTemps, nightTemps };
}

export function clearChart() {
  if (temperatureChart) {
    temperatureChart.destroy();
    temperatureChart = null;
  }
}
