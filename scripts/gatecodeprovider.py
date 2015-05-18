#!/usr/bin/env python
import rospy
import requests
import json
import sys
import time
from std_msgs.msg import String



def callback(data):

	global course 

	course = data.data

def callbacktwo(data):
	try:

		mainUrl = data.data

		#the last part of the link needs to be removed i.e.
		# the actual link is: /obstacleAvoidance/%s/UF
		#this is just to test on my server

		sublinkMain = '/obstacleAvoidance/%s/UF/gateCode.json' %course

		url = mainUrl +  sublinkMain

		print(url)

		r = requests.get(url)	
				
		if(r.status_code == 200):
				
			gatecode_all = r.json()['gateCode']

			temp = gatecode_all.split(",")

			entrance = temp[0].replace("(","")

			exit = temp[1].replace(")","")

			gatecode = "{'entrance':'%s','exit':'%s'}" %(entrance, exit)	

			#it publishes a dictioanry as a string type to the topic
			# e.g {'etrance':'3','exit':'Y'}

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
	
	except rospy.ServiceException:
		
		main()		

def main():

	rospy.init_node('gatecodeprovider')

	rospy.Subscriber('course_code', String, callback)

	time.sleep(5)

	rospy.Subscriber('main_server_url', String, callbacktwo)

	rospy.spin()

if __name__ == '__main__':

	try:

		main()

	except (rospy.ROSInterruptException, rospy.ServiceException) as e:
		
		pass	