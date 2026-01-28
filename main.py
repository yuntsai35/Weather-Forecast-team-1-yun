import os
from dotenv import load_dotenv
load_dotenv()

import datetime
import requests as remote_requests

from fastapi import * 
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import datetime
from datetime import timezone
app=FastAPI()

app.mount("/page", StaticFiles(directory="page"), name="page")

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./page/index.html", media_type="text/html")


api_key=os.getenv("CWB_API_KEY")

#一般天氣預報-今明36小時天氣預報
@app.get("/v1/rest/datastore/F-C0032-001")
async def get_weather_36h(request: Request, locationName: str=None):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&format=JSON'
    
    if locationName:
       url += f'&locationName={locationName}'
    
    response=remote_requests.get(url,verify=False, timeout=10)

    if response.status_code != 200:
        return {"error": "無法取得氣象資料"}

    data_json = response.json()
    data_json = data_json['records']['location']

    All_data =[]

    for item in data_json:

        location = item['locationName']
        elements = item['weatherElement']

        #Wx
        Wx = elements[0]
        first_list=Wx['time'][0]
        parameterName_Wx=first_list['parameter']['parameterName']
        parameterValue_Wx=first_list['parameter']['parameterValue']

        #MinT
        MinT = elements[2]
        first_list=MinT['time'][0]
        parameterName_MinT=first_list['parameter']['parameterName']
        parameterValue_MinT=first_list['parameter']['parameterUnit']

        #MaxT
        MaxT = elements[4]
        first_list=MaxT['time'][0]
        parameterName_MaxT=first_list['parameter']['parameterName']
        parameterValue_MaxT=first_list['parameter']['parameterUnit']

        #POP
        PoP = elements[1]
        first_list=PoP['time'][0]
        parameterName_PoP=first_list['parameter']['parameterName']
        parameterValue_POP=first_list['parameter']['parameterUnit']
 
        city_info = {
            "locationName": location,
            "Wx":  parameterName_Wx,
            "MinT": parameterName_MinT,
            "MaxT":parameterName_MaxT,
            "PoP": parameterName_PoP
        }
        All_data.append(city_info)


    return {"success": True, "data": All_data}


#Weekly

city_codes = {
    "003": "宜蘭縣", "007": "桃園市", "011": "新竹縣", "015": "苗栗縣",
    "019": "彰化縣", "023": "南投縣", "027": "雲林縣", "031": "嘉義縣",
    "035": "屏東縣", "039": "臺東縣", "043": "花蓮縣", "047": "澎湖縣",
    "051": "基隆市", "055": "新竹市", "059": "嘉義市", "063": "臺北市",
    "067": "高雄市", "071": "新北市", "075": "臺中市", "079": "臺南市",
    "083": "連江縣", "087": "金門縣", "091": "台灣全島"
}


def data_process(data_json):
    
    data_json = data_json['records']['Locations'][0]['Location']
    All_Town_data =[]

    for item in data_json:
        LocationName = item['LocationName']
        Geocode = item['Geocode']
        Latitude = item['Latitude']
        Longitude = item['Longitude']
        WeatherElement = item['WeatherElement']


        temp_times = WeatherElement[0]['Time']
        humi_times = WeatherElement[4]['Time']
        rain_times = WeatherElement[11]['Time']
        clim_times = WeatherElement[12]['Time']

        all_times_town = []

        for i in range(len(temp_times)):
            startTime = temp_times[i]['StartTime']
            endTime = temp_times[i]['EndTime'] 
            
            Temperature = temp_times[i]['ElementValue'][0]['Temperature']
            RelativeHumidity = humi_times[i]['ElementValue'][0]['RelativeHumidity']
            ProbabilityOfPrecipitation = rain_times[i]['ElementValue'][0]['ProbabilityOfPrecipitation']
            Weather = clim_times[i]['ElementValue'][0]['Weather']

            
            time_data = {
                "startTime": startTime,
                "endTime": endTime,
                "Temperature": Temperature,
                "RelativeHumidity": RelativeHumidity,
                "ProbabilityOfPrecipitation": ProbabilityOfPrecipitation,
                "Weather": Weather
            }
            
            all_times_town.append(time_data)

        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)

    return All_Town_data

#鄉鎮天氣預報-鄉鎮市區未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-{city_id}")
async def get_weekly_forecast(city_id: str, LocationName: str = None):

    if city_id not in city_codes:
        return JSONResponse(status_code=404, content={"success": False, "message": "無效的縣市代碼"})

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-{city_id}?Authorization={api_key}'

    if LocationName:
      url += f'&LocationName={LocationName}'

    data=remote_requests.get(url, verify=False, timeout=10)
    data_json = data.json()

    processed_data = data_process(data_json)

    return {"success": True, "data": processed_data}



#Rain Amount
@app.get("/v1/rest/datastore/O-A0002-001")
async def get_rain_amount(request: Request, station_id: str = None):
    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization={api_key}'
    
    if station_id:
        url += f'&StationId={station_id}'

    data=remote_requests.get(url, verify=False, timeout=10)
    data_json = data.json()
    
    if 'Station' not in data_json['records']:
        return {"success": False, "message": "找不到對應的站點資料"}

    data_json = data_json['records']['Station']
    
    Rainfall_data=[]

    for item in data_json:
        #place
        CountyName=item['GeoInfo']['CountyName']
        TownName=item['GeoInfo']['TownName']
        StationName = item['StationName'] 
        StationId = item['StationId']

        #rain info
        RainfallElement=item['RainfallElement']
        Now=RainfallElement['Now']['Precipitation']
        Past10Min=RainfallElement['Past10Min']['Precipitation']
        Past1hr=RainfallElement['Past1hr']['Precipitation']
        Past3hr=RainfallElement['Past3hr']['Precipitation']
        Past6Hr=RainfallElement['Past6Hr']['Precipitation']
        Past12hr=RainfallElement['Past12hr']['Precipitation']
        Past24hr=RainfallElement['Past24hr']['Precipitation']
        Past2days=RainfallElement['Past2days']['Precipitation']
        Past3days=RainfallElement['Past3days']['Precipitation']   
        
        data={"CountyName":CountyName, "TownName":TownName, "StationName": StationName, "StationId": StationId, "Now":Now, "Past10Min":Past10Min,
              "Past1hr":Past1hr, "Past3hr":Past3hr,"Past6Hr":Past6Hr, "Past12hr":Past12hr,"Past24hr":Past24hr, "Past2days":Past2days,"Past3days":Past3days}

        Rainfall_data.append(data)

    return {"success": True, "data": Rainfall_data}
