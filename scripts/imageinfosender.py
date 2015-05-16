#!/usr/bin/env python
import rospy
import sys
import requests
import json
from std_msgs.msg import String

global course
global shape
global imageID

def callback(data):

	#receive the current course e.g. "courseA"
	# and store it in "course"

	course = data.data

def callbacktwo(data):

	#receive image ID and store it in "imageID"

	imageID = data.data

def callbackthree(data):	

	# receive the shape and store it in "shape"

	shape = data.data	

def callbackfour(data):

	mainUrl = data.data

	sublinkMain = '/interop/report/%s/UF' %course

	#creating url

	url = mainUrl +  sublinkMain
	
	#ready payload to send to server..

	payload = '{"course": "%s","team":"UF","shape":"%s","imageID":"%s"}' %(course, shape, imageID)

	# create request object

	r = requests.post(url, data = payload)

	#decode json response froms server

	satus = r.json()['success']

	# define topic for publishing status

	status_pub = rospy.Publisher('image_rec_success_status', String, queue_size=10)

	if status == 'false':

		rospy.loginfo(status)

		status_pub.publish(status)

		return

# if false is returned by the server, i.e. the image shape was not correctly
# identified, publish  to the topic and let the boat know
# so the image is processed again and exit		

	else:	

		while not rospy.is_shutdown():

			rospy.loginfo(status)

			# we're all good, publish true forever

			status_pub.publish(status)


def main():

	rospy.init_node('imageinfopublisher')

	######## TOPIC SUBSCRIPTION ##########

	rospy.Subscriber('course_code', String, callback)

	# receives the image id sent by the server
	# when the picture taken by the drone was uploaded. 

	rospy.Subscriber('image_id', String, callbacktwo)

	# receives the shape from the photo the drone took and the boar
	# decoded. e.g. "E" 

	rospy.Subscriber('image_shape', String, callbackthree)

	#receives the main url to which the inforation regarding the image
	#will be posted

	rospy.Subscriber('main_server_url', String, callbackfour)

	
	rospy.spin()

if __name__ == '__main__':
	
	try:
	
		main()
	
	except (rospy.ROSInterruptException, IndexError, NameError, rospy.ServiceException) as e:
		pass	