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
	
	mainUrl = data.data

	sublinkMain = '/automatedDocking/%s/UF' %course

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
			
			dockingBay1_symbol_pub = rospy.Publisher('docking_bay1_symbol', String, queue_size=10)
			
			dockingBay1_color_pub = rospy.Publisher('docking_bay1_color', String, queue_size=10)
			
			dockingBay2_symbol_pub = rospy.Publisher('docking_bay2_symbol', String, queue_size=10)
			
			dockingBay2_color_pub = rospy.Publisher('docking_bay2_color', String, queue_size=10)
			
			rate = rospy.Rate(1)
			
			while not rospy.is_shutdown():
				
				rospy.loginfo(firstDockSymbol)
				
				rospy.loginfo(firstDockColor)
				
				rospy.loginfo(secondDockSymbol)
				
				rospy.loginfo(secondDockColor)
				
				dockingBay1_symbol_pub.publish(firstDockSymbol)
				
				dockingBay1_color_pub.publish(firstDockColor)
				
				dockingBay2_symbol_pub.publish(secondDockSymbol)
				
				dockingBay2_color_pub.publish(secondDockColor)
				
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
	
	rospy.spin()

if __name__ == '__main__':
	
	try:
	
		main()
	
	except (rospy.ROSInterruptException, rospy.ServiceException) as e:

			pass		

