#!/usr/bin/env python
import rospy
import sys
import requests
import shutil
import json
import os
import time
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage


# custom iterator

def my_range(start, end, step):
    while start < end:
        yield start
        start += step

#Store the server's ip address        

def StoreServerUrl(ServerUrl):

	global mainUrl

	try:

		mainUrl = ServerUrl.data

	except NameError:
		pass		

#store the course info

def StoreCourseInfo(courseInfo):

	global course

	try:

		course = courseInfo.data

	except NameError:
		pass 	

	
def generateRequests():

	

	# main sublink

	sublinkMain = '/interop/images/%s/UF/imageList.htm' %course

	print (sublinkMain)

	#creating url

	url = mainUrl +  sublinkMain

	print (url)

	#headers need to be specified!
	#my server does not support headers
	#this needs to be tested
	
	#### UNCOMMENT headers #####

	#headers = 'Content-Type: text/html'

	#creating request object

	try:

		try:

			r = requests.get(url)
			### Request with headers ###
			# r = requests.get(url, headers = headers)

		except ConnectionError:

			generateRequests()

	except NameError:
		
		main()			

	time.sleep(2)

	try:

		if r.status_code == 200:

			print (r.text)

			string = r.text

			links = string.split('"')

			links2 = []

			imageNames = []

			counter = -1

			for index in my_range(0, len(links), 1):
			    
			    if index % 2 != 0:
			 
			    	links2.append(links[index])

			for sublink in links2:
				
				imageNames.append(sublink.split("/")[3])

			global imgCount

			imgCount = 0		
			
			for sublink in links2:
				
				requestLink = mainUrl + sublink

				counter = counter + 1

				imageName = imageNames[counter]


				

					#after having parsed the html that the server returned
					# this generates as many requests as links the server provides
					#and saves the images to ~/output/images/pngs/
					
				time.sleep(3)

				r = requests.get(requestLink, stream = True)

				path = os.path.join(os.path.expanduser('~'), 'output', 'ServerImages/')
					
				with open(path+imageName,'wb') as out_file:
					
					shutil.copyfileobj(r.raw, out_file)
					
				del r

				imgCount = imgCount + 1
					

			status_pub = rospy.Publisher('server_images_info', String, queue_size=10)	

			rate = rospy.Rate(1)
			
			while not rospy.is_shutdown():

				data = "{'images':'%s'}" % imgCount

				rospy.loginfo(data) 
				
				status_pub.publish(data) 
				
				rate.sleep()	

		else:
			
			raise rospy.ServiceException("Bad Request")		



	except rospy.ServiceException:

		time.sleep(5)

		generateRequests()		


def main():
	
	rospy.init_node('from_server_image_getter')	

	#no drone challege, where we receive an image list
	# in html and each request needs to be done separately
	# and we have to process and identify one of them

	rospy.Subscriber('main_server_url', String, StoreServerUrl) 

	rospy.Subscriber('course_code', String, StoreCourseInfo)

	time.sleep(5)	

	generateRequests()

	rospy.spin()	

if __name__ == '__main__':

	try:
	
		main()

	except rospy.ROSInterruptException:
		pass	

