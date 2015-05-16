#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String



def ScanMainUrl():
	
	mainurl = raw_input("What is the MAIN server URL?: ")
	
	return mainurl

def ScanCourseCode():

	coursecode = raw_input("What COURSE are we attempting?: ")
	
	return coursecode


def main():

	mainurl = ScanMainUrl()

	coursecode = ScanCourseCode()

	mainurl_pub = rospy.Publisher('main_server_url', String, queue_size=10)
	
	coursecode_pub = rospy.Publisher('course_code', String, queue_size=10)
	
	rospy.init_node('urlandcourseprovider')
	
	rate = rospy.Rate(20)

	while not rospy.is_shutdown():
		
		rospy.loginfo(mainurl)
		
		rospy.loginfo(coursecode)
		
		mainurl_pub.publish(mainurl)
		
		coursecode_pub.publish(coursecode)
		
		rate.sleep()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass	