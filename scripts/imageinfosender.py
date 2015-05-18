#!/usr/bin/env python
import rospy
import sys
import requests
import json
import os
import time
from std_msgs.msg import String


def StoreCourseInfo(courseInfo):

	#receive the current course e.g. "courseA"
	#and store it in "course"

	global course

	try:

		course = courseInfo.data

	except NameError:
		pass	

def StoreServerUrl(data):

	#receive server url and store it in
	#mainUrl

	global mainUrl

	try:

		mainUrl = data.data

	except NameError:
		pass	

def SendImageInfo(imageName, imageShape):

	imageName = imageName

	shape = imageShape

	postImageLink = '/interop/image/%s/UF' %course

	sendImageInfoLink = '/interop/report/%s/UF' %course

	#creating urls

	putImageOnServerUrl = mainUrl +  postImageLink

	sendImageInfoUrl = mainUrl +  sendImageInfoLink

	###################################### put image on server #############################################

	global path


	path = os.path.join(os.path.expanduser('~'), 'output', 'ServerImages', imageName)


	files = {'file': (imageName, open(path, 'rb'), 'multipart/mixed', {'Expires': '0'})}

	#Send image to server and get an image ID.
	# create request #2 (POST), put image file on server

	request1 = requests.post(putImageOnServerUrl, files=files, verify=False)

	#getting image ID from server. Will be a json structure like:
	#{"id":"a4aa8224-07f2-4b57-a03a-c8887c2505c7"}
	# wait two second... just for the heck of it
	time.sleep(2)

	imageID = request1.json['id']


	#########################################################################################################

	######################################## send image information #########################################	
			
	#ready payload to send to server..



	payload = '{"course":"%s","team":"UF","shape":"%s","imageID":"%s"}' %(course, shape, imageID)

	# create request #2, post image info json structure

	request2 = requests.post(url, data = json.dumps(payload))

	#decode json response from server

	status = r.json()['success']

	#return status from server to know whether the right
	#image was sent

	return status

# if false is returned by the server, i.e. the image shape was not correctly
# identified, return said status so that node in charge of image 
# analysing send another image name

def send_image_info_server():

	
	rospy.init_node('send_image_info_server')

	rospy.Subscriber('course_code', String, StoreCourseInfo)

	rospy.Subscriber('main_server_url', String, StoreServerUrl)
	
	s = rospy.Service('send_image_info', ImageInfo, SendImageInfo)

	print('ready to receive image info')

	time.sleep(5)

	rospy.spin()

if __name__ == '__main__':
	

	send_image_info_server()
	
	