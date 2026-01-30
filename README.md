# 全國即時氣象

全國即時氣象是一個天氣預報網站，提供各縣市即時及當週的天氣預報和降雨量資訊。

## 網站功能
- 點擊地圖各縣市，呈現指定區域當日天氣預報
- 點擊查看各鄉鎮市區可進階篩選查看一週天氣
- 點擊雨量觀測可查看各縣市即時雨量觀測資料
- 點擊按鈕可將指定區域一週天氣發送至 Discord

![Demo](/page/image/Demo.gif)

## 使用技術
- 前端使用：HTML、CSS、JavaScript、D3.js、Chart.js
- 後端使用：Python、FastAPI、MVC 模式檔案管理
- 使用 Git Flow 掌控開發流程及版本控制
- 串接 Discord Webhook
- 使用 AWS EC2 部署網站

## 團隊分工
#### **組長 / 黃良樺｜前端開發**
- 研究並使用 D3.js 函式庫
- 完成互動式台灣地圖
- 與前端討論如何相互串接
- 與後端溝通 API 回傳資料格式
- 協調 Pull requests 檔案合併衝突問題
- README 文件共同撰寫
- AWS EC2 網站佈署上線
- 成果報告

**陳羿如｜前端開發**
- 功能發想，分工討論
- 介面設計及定義設計規範
- 與前端討論如何相互串接
- 與後端溝通 API 回傳資料格式
- 研究並使用 Chart.js 函式庫
- 選單、資料表格動態生成
- 協助 UI / UX 優化
- README 文件共同撰寫

**蔡紜潔｜後端開發**
- 與前端溝通 API 回傳資料格式
- 串接中央氣象 API 並彙整資料
- 天氣預報的 API 設計與實現
- 降雨量 API 的設計與實現
- 串接 Discord Webhook
- README 文件共同撰寫

## 資料來源
- [中央氣象署開放資料](https://opendata.cwa.gov.tw/dist/opendata-swagger.html)