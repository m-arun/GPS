import serial,ast
import pynmea2
import json,geojson
import requests
import time

ser = serial.Serial('/dev/ttyUSB1',9600,timeout = None)
 
geoJson = {}
geoJson["geolocation"] ={}
geoJson["geolocation"] = []

geoPoint = {}
geoPoint["geometry"] = {}
geoPoint["geometry"]["type"] = "Point"
geoPoint["geometry"]["coordinates"] = [77.570359, 13.014114]
geoPoint["type"] = "Feature"
geoPoint["properties"] = {}

geoJson["geolocation"].append(geoPoint)
#reg = json.dumps(geoJson, ensure_ascii=False)

publish_url = "https://smartcity.rbccps.org/api/1.0.0/publish"
publish_headers = {"apikey": "0e7c05eb6a7a4e82adb2569600afe29b"}
publish_data = {
                "body": str(geoJson)
		#reg = json.dumps(geoJson, ensure_ascii=False)

	        #"body": json.dumps(geoJson, ensure_ascii=False)
		#"body": reg
			
  	       }

while 1:
        gps = ser.readline()
        words = gps.split(",")
        if "$GNGGA" in words:
                msg = pynmea2.parse(gps)
		
		geoPoint["geometry"]["coordinates"] = [msg.longitude if msg.longitude != 0.0 else 77.570359,msg.latitude if msg.latitude != 0.0 else  13.014114]
		r = requests.post(publish_url, json.dumps(geoJson), headers=publish_headers,verify=False)
		response = dict()
		if "No API key" in str(r.content.decode("utf-8")):
			response["status"] = "failure"
			r = json.loads(r.content.decode("utf-8"))['message']
		elif 'Publish message OK\n' in str(r.content.decode("utf-8")):
			response["status"] = "success"
			r = r.content.decode("utf-8")
		else:
			response["status"] = "failure"
			r = r.content.decode("utf-8")
			response["response"] = str(r)
		print response
		print geoJson
