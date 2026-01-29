const discord = document.querySelector("#discord-btn");
discord.addEventListener("click", async function () {
  const cityText = document.querySelector(
    "#county-btn .dropdown__text"
  ).textContent;
  const areaText = document.querySelector(
    "#area-btn .dropdown__text"
  ).textContent;

  if (cityText === "選擇縣市") {
    alert("請選擇縣市");
    return;
  }
  if (areaText === "選擇鄉鎮市區") {
    alert("請選擇鄉鎮市區");
    return;
  }

  let response = await fetch("/sendWebhook", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ cityText: cityText, areaText: areaText }),
  });
  let result = await response.json();

  if (response.ok) {
    alert("成功發送資料到Discord !");
  }
});
