import os
from dotenv import load_dotenv
load_dotenv()

import requests

api_key=os.getenv("CWB_API_KEY")

location={}
url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}'
data=requests.get(url)
data_json = data.json()
data_json = data_json['records']['location']


All_data = []

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



url2 = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-003?Authorization={api_key}'
data=requests.get(url2)
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

    all_times_for_this_town = []

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
        all_times_for_this_town.append(time_data)

    # 4. 最後將整個行政區及其「所有時間組」存入總清單
    town_info = {
        "LocationName": LocationName,
        "Time": all_times_for_this_town
    }
    
    All_Town_data.append(town_info)

print(All_Town_data)









