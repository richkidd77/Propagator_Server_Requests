#!/usr/bin/env python
import rospy
import sys
import requests
import json
from datetime import datetime
from time import strftime
from std_msgs.msg import String

global mainUrl
global course


def callback(data):

	mainUrl = data.data

def callbacktwo(data):
	
	course = data.data	

def callbackthree(data):

	while not rospy.is_shutdown():

		#Gps data needs to be in decimal degrees
		#being published to the topic 
		#preferably as "latitude,longitde" ###Notice comma###

		gpsData = data.data
		
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

	rospy.Subscriber('main_server_url', String, callback)

	rospy.Subscriber('course_code', String, callbacktwo)

	rospy.Subscriber('gps_data', String, callbackthree)
	
	 
	
	rospy.spin()

if __name__ == '__main__':
	
	try:
		
		main()
	
	except (rospy.ROSInterruptException, IndexError, NameError, rospy.ServiceException) as e:
		pass