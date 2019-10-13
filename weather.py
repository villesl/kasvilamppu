#!/usr/bin/python3
import requests, re, os
from datetime import time, datetime, timezone, timedelta

tnow = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
tplus15 = (datetime.now(timezone.utc) + timedelta(minutes = 15)).strftime("%Y-%m-%dT%H:%M:%SZ")
tminus15 = (datetime.now(timezone.utc) - timedelta(minutes = 15)).strftime("%Y-%m-%dT%H:%M:%SZ")
now_time = (datetime.now()).time()

def weather_get(metric, start, end):
    p1 = requests.get('http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::simple&timestep=1&starttime='+start+'&endtime='+end+'&place=Kallio,Helsinki&parameters='+metric)
    p2 = re.findall('<BsWfs:ParameterValue>(.*?)<\/BsWfs:ParameterValue>',p1.content.decode('utf-8'))
    p3 = list(map(float, p2))
    return round((sum(p3) / float(len(p3))),2)
cloud30 = weather_get('TotalCloudCover',tminus15,tplus15)
rain15 = weather_get('Precipitation1h',tnow,tplus15)

f = open("cloud.log","a")
f.write(tnow+"\t"+str(cloud30)+"\t"+str(rain15)+"\n")
f.close()

if rain15 > 0.5:
    os.system("/usr/local/bin/tplink-smarthome-api setPowerState 0")
    os.system("/usr/local/bin/tplink-smarthome-api setPowerState 1")
    os.system("/usr/local/bin/tplink-smarthome-api setPowerState 0")
    os.system("/usr/local/bin/tplink-smarthome-api setPowerState 1")

if now_time >= time(18,00) or now_time <= time(8,00):
    os.system("/usr/local/bin/tplink-smarthome-api setPowerState 0")
elif cloud30 >= 65:
    os.system("/usr/local/bin/tplink-smarthome-api setPowerState 1")
elif cloud30 < 65:
    os.system("/usr/local/bin/tplink-smarthome-api setPowerState 0")