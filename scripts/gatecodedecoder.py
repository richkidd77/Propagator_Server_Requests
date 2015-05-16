#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String

def callback(data):
	entrance = None
	exit = None
	gateCode = data.data

	if(gateCode == '(1,X)'):
		entrance = '1'
		exit = 'X'
	elif(gateCode == '(1,Y)'):
		entrance = '1'
		exit = 'Y'
	elif(gateCode =='(1,Z)'):
		entrance = '1'
		exit = 'Z'
	elif(gateCode == '(2,X)'):
		entrance = '2'
		exit = 'X'
	elif(gateCode == '(2,Y)'):
		entrance = '2'
		exit = 'Y'
	elif(gateCode =='(2,Z)'):
		entrance = '2'
		exit = 'Z'
	elif(gateCode == '(3,X)'):
		entrance = '3'
		exit = 'X'
	elif(gateCode == '(3,Y)'):
		entrance = '3'
		exit = 'Y'
	elif(gateCode =='(3,Z)'):
		entrance = '3'
		exit = 'Z'
	gatecode_entrance_pub = rospy.Publisher('gate_code_entrance', String, queue_size=10)
	gatecode_exit_pub = rospy.Publisher('gate_code_exit', String, queue_size=10)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		rospy.loginfo(entrance)
		gatecode_entrance_pub.publish(entrance)
		rospy.loginfo(exit)
		gatecode_exit_pub.publish(exit)
		rate.sleep()	

def main():

	rospy.init_node('gatecodedecoder')
	rospy.Subscriber('gate_code', String, callback)
	rospy.spin()

if __name__ == '__main__':
	try:
		main()	
	except rospy.ROSInterruptException:
		pass	