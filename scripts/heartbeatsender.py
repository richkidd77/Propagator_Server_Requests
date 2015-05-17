#!/usr/bin/env python
import rospy
import sys
import requests
import json
from datetime import datetime
from time import strftime
from std_msgs.msg import String


#### Need to figure out a way to get gps data from boat and turn it
### into decimal degreed to send to server

### need to alsog get current task


def StoreServerUrl(serverUrl):

	global mainUrl

	mainUrl = serverUrl.data

rospy.Subscriber('main_server_url', String, storeMainServerUrl)

def StoreCourseInfo(courseInfo):

	global course
	
	course = courseInfo.data

rospy.Subscriber('course_code', String, StoreCourseInfo)

def GetGpsData(gpsPos):

	###Need to format gpsData so it is latitude, longitude

	global gpsData 

	gpsData = gpsPos.data

rospy.Subscriber('gps_data', String, GetGpsData)	

def SendHeartBeat():

	while not rospy.is_shutdown():

		#Gps data needs to be in decimal degrees
		#being published to the topic 
		#preferably as "latitude,longitde" ###Notice comma###
		
		gpsDataList = gpsData.split(",")

		timeStamp1 = datetime.utcnow()

		timeStamp2 = timeStamp1.strftime('%Y%m%d%H%M%S')

		latitude = gpsDataList[0]

		longitude = gpsDataList[1]

		realLatitude = latitude[0:9]

		realLongitude = longitude[0:10]	

		latitudeFinal = float(realLatitude)

		longitudeFinal = float(realLongitude)

		sublinkMain = '/heartbeat/%s/UF' %course

		url = mainUrl +  sublinkMain

		payload = '{"timestamp":"%s", "challenge":"%s","position":{"datum":"WGS84","latitude":"%s","longitude":"%s"}}' % (timeStamp2, currentChallenge, latitudeFinal,longitudeFinal)

		heartbeat_pub = rospy.Publisher('gps_heartbeat', String, queue_size=10)
		
		rate = rospy.Rate(1)
		
		r = requests.post(url, data = payload)

		if(r.status_code == 200 and r.json()['success'] == 'true'):

			rospy.loginfo(payload)

			heartbeat_pub.publish(payload)

			print(r.headers)

			print(r.text)

			rate.sleep()

		else:

			raise rospy.ServiceException('SomethingWrong')	

def main():
	
	rospy.init_node('heartbeat')

	SendHeartBeat()
	
	rospy.spin()

if __name__ == '__main__':
	
	try:
		
		main()
	
	except rospy.ROSInterruptException:
		pass