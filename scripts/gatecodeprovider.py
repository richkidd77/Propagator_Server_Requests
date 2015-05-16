#!/usr/bin/env python
import rospy
import requests
import json
import sys
from std_msgs.msg import String

global course 

def callback(data):

	course = data.data

def callbacktwo(data):
	try:

		mainUrl = data.data

		sublinkMain = '/obstacleAvoidance/%s/UF' %course

		url = mainUrl +  sublinkMain

		r = requests.get(url)	
				
		if(r.status_code == 200):
				
			gatecode_all = r.json()['gateCode']

			temp = gatecode.split(",")

			entrace = temp[0].replace("(","")

			exit = temp[1].replace(")","")

			gatecode = "ENTRANCE:%s EXIT:%s" %(entrance, exit)	

			gatecode_pub = rospy.Publisher('gate_code', String, queue_size=10)
			
			rate = rospy.Rate(1)
			
			while not rospy.is_shutdown():

				rospy.loginfo(gatecode)
				
				gatecode_pub.publish(gatecode)
				
				rate.sleep()
		
		elif(r.status_code == 400):

			raise rospy.ServiceException('BadRequest')
		
		elif(r.status_code == 404):

			raise rospy.ServiceException('TeamOrCourseNotFound')
		
		elif(r.status_code == 500):

			raise rospy.ServiceException('GateIsBroken')
		
		else:

			raise rospy.ServiceException('SomethingWrong')
	
	except rsopy.ServiceException:
		
		main()		

def main():

	rospy.init_node('gatecodeprovider')

	rospy.Subscriber('course_code', String, callback)

	rospy.Subscriber('main_server_url', String, callbacktwo)

	rospy.spin()

if __name__ == '__main__':

	try:

		main()

	except (rospy.ROSInterruptException, rospy.ServiceException) as e:
		
		pass	