#!/usr/bin/env python
import rospy
import requests
import json
import sys
import time
from std_msgs.msg import String

global course
global mainUrl


def callback(data):

	global course

	try:
		
		course = data.data
	
	except NameError:
		pass

def callbacktwo(data):

	global mainUrl
	
	try:

		mainUrl = data.data

	except NameError:
		pass	

def postDockingSequence():	

	sublinkMain = '/automatedDocking/%s/UF/docking.json' %course

	url = mainUrl +  sublinkMain

	r = requests.get(url) #creating request object
	
	#evaluating response status code

	try:
	
		if(r.status_code == 200):

			dataList = r.json()['dockingBaySequence']
			
			firstDockInfo = dataList[0]
			
			secondDockInfo = dataList[1]
			
			firstDockSymbol = firstDockInfo['symbol']
			
			firstDockColor = firstDockInfo['color']
			
			secondDockSymbol = secondDockInfo['symbol']
			
			secondDockColor =  secondDockInfo['color']

			infoToPublish = "{'firstDockSymbol': '%s','firstDockColor':'%s','secondDockSymbol':'%s','secondDockColor':'%s'}" %(firstDockSymbol, firstDockColor,secondDockSymbol,secondDockColor) 
			
			docking_sequence_pub = rospy.Publisher('docking_bay_sequence', String, queue_size=10)
			
			rate = rospy.Rate(1)
			
			while not rospy.is_shutdown():
				
				rospy.loginfo(infoToPublish)
				
				docking_sequence_pub.publish(infoToPublish)
				
				rate.sleep()
		
		elif(r.status_code == 400):
		
			raise rospy.ServiceException('BadRequest')
		
		elif(r.status_code == 404):
		
			raise rospy.ServiceException('TeamOrCourseNotFound')
		
		elif(r.status_code == 500):
		
			raise rospy.ServiceException('GateIsBroken')

	except rospy.ServiceException:
		
		main()	
				

def main():
	
	rospy.init_node('dokcingbayprovider')
	
	rospy.Subscriber('course_code', String, callback)

	rospy.Subscriber('main_server_url', String, callbacktwo)

	time.sleep(5)

	postDockingSequence()
	
	rospy.spin()

if __name__ == '__main__':
	
	try:
	
		main()
	
	except rospy.ROSInterruptException:

		pass		

