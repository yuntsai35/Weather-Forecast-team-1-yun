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

app.mount("/static", StaticFiles(directory="page"), name="page")

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./page/index.html", media_type="text/html")


api_key=os.getenv("CWB_API_KEY")

#一般天氣預報-今明36小時天氣預報
@app.get("/v1/rest/datastore/F-C0032-001")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&format=JSON'
    response=remote_requests.get(url)

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

#鄉鎮天氣預報-宜蘭縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-003")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-003?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-桃園市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-007")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-007?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}


#鄉鎮天氣預報-新竹縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-011")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-011?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}


#鄉鎮天氣預報-苗栗縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-015")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-015?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}


#鄉鎮天氣預報-彰化縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-019")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-019?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-南投縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-023")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-023?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}


#鄉鎮天氣預報-雲林縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-027")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-027?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}


#鄉鎮天氣預報-嘉義縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-031")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-031?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}


#鄉鎮天氣預報-屏東縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-035")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-035?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}


#鄉鎮天氣預報-臺東縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-039")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-039?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}


#鄉鎮天氣預報-花蓮縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-043")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-043?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-澎湖縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-047")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-047?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-基隆市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-051")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-051?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-新竹市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-055")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-055?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-嘉義市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-059")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-059?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-台北市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-063")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-063?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-高雄市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-067")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-067?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-新北市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-071")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-071?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-台中市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-075")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-075?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-台南市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-079")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-079?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-連江縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-083")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-083?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}

#鄉鎮天氣預報-金門縣未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-087")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-087?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}


#鄉鎮天氣預報-台灣全島縣市未來一週天氣預報
#平均相對濕度, 12小時降雨機率, 平均溫度, 天氣現象(未來一周)
@app.get("/v1/rest/datastore/F-D0047-091")
async def attraction(request: Request):

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization={api_key}'
    data=remote_requests.get(url)
    data_json = data.json()
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
            
            # 加進該行政區的時間清單中
            all_times_town.append(time_data)

        # 4. 最後將整個行政區及其「所有時間組」存入總清單
        town_info = {
            "LocationName": LocationName,
            "Time": all_times_town
        }
    
        All_Town_data.append(town_info)


    return {"success": True, "data": All_Town_data}






