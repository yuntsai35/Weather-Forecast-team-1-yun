import os
from dotenv import load_dotenv
load_dotenv()

import requests as remote_requests
from dhooks import Webhook, Embed
from fastapi import * 
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

import data as weatherdata

router = APIRouter()

api_key=os.getenv("CWB_API_KEY")
discord=os.getenv("DISCORD_URL2")
hook= Webhook(discord)

city_codes = {
    "003": "宜蘭縣", "007": "桃園市", "011": "新竹縣", "015": "苗栗縣",
    "019": "彰化縣", "023": "南投縣", "027": "雲林縣", "031": "嘉義縣",
    "035": "屏東縣", "039": "臺東縣", "043": "花蓮縣", "047": "澎湖縣",
    "051": "基隆市", "055": "新竹市", "059": "嘉義市", "063": "臺北市",
    "067": "高雄市", "071": "新北市", "075": "臺中市", "079": "臺南市",
    "083": "連江縣", "087": "金門縣", "091": "台灣全島"
}


#一般天氣預報-今明36小時天氣預報
@router.get("/v1/rest/datastore/F-C0032-001")
async def get_weather_36h(request: Request, locationName: str=None):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&format=JSON'
    
    if locationName:
       url += f'&locationName={locationName}'
    
    response=remote_requests.get(url,verify=False, timeout=10)

    if response.status_code != 200:
        return {"error": "無法取得氣象資料"}

    data_json = response.json()
    processed_data = weatherdata.weather_36hr(data_json)

    return {"success": True, "data": processed_data}


#鄉鎮天氣預報-鄉鎮市區未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@router.get("/v1/rest/datastore/F-D0047-{city_id}")
async def get_weekly_forecast(city_id: str, LocationName: str = None):

    if city_id not in city_codes:
        return JSONResponse(status_code=404, content={"success": False, "message": "無效的縣市代碼"})

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-{city_id}?Authorization={api_key}'

    if LocationName:
      url += f'&LocationName={LocationName}'

    data=remote_requests.get(url, verify=False, timeout=10)
    data_json = data.json()

    processed_data = weatherdata.data_process(data_json)

    return {"success": True, "data": processed_data}


#Rain Amount
@router.get("/v1/rest/datastore/O-A0002-001")
async def get_rain_amount(request: Request, station_id: str = None):
    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization={api_key}'
    
    if station_id:
        url += f'&StationId={station_id}'

    data=remote_requests.get(url, verify=False, timeout=10)
    data_json = data.json()
    
    if 'Station' not in data_json['records']:
        return {"success": False, "message": "找不到對應的站點資料"}

    Rainfall_data = weatherdata.rainfall_data(data_json)

    return {"success": True, "data": Rainfall_data}

#Discord Webhook
@router.post('/sendWebhook')
def get_weekly_weather(body: dict = Body(...)):

    countyName=body["cityText"]
    townName=body["areaText"]

    countyId = None
    for k, v in city_codes.items():
        if v == countyName:
            countyId = k 
            break

    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization={api_key}&format=JSON&locationId=F-D0047-{countyId}&LocationName={townName}&ElementName="
    response = remote_requests.get(url,verify=False, timeout=10)
    data_json = response.json()

    countyName=city_codes[countyId]

    embed=Embed(title=f'🌟 {countyName}{townName} 白天一週天氣預報', color=505058, timestamp='now')

    weather_data = weatherdata.discord_data(data_json)

    for data in weather_data:

        field_name= f'> **{data["date"]}**'
        field_value = (
                f"🌡️ 溫度 {data["Temperature"]} ℃\n"
                f"💧 濕度 {data["RelativeHumidity"]}%\n"
                f"🌧️ 降雨 {data["ProbabilityOfPrecipitation"]}%\n"
                f"☀️ 天氣 {data["Weather"]}"
                    )
        embed.add_field(name=field_name, value=field_value, inline=True)

    radar_url = "https://cdn.discordapp.com/attachments/1465949592800591894/1466133485885329448/beautiful-pink-sakura.jpg?ex=697ba2b6&is=697a5136&hm=7a6d5a0e9bdedd5b713bfcae61f9e93c9f94bbf84c35048dff3b25aac838c191&" 
    embed.set_image(url=radar_url)

    embed.set_footer(text='資料來源: 中央氣象局')
    hook.send("# 感謝您使用本網站 😊\n以下為一週白天天氣預報", embeds=[embed]) 