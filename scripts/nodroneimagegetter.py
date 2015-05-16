#!/usr/bin/env python
import rospy
import sys
import requests
import shutil
import json
import os
import time
from std_msgs.msg import String



# custom iterator

def my_range(start, end, step):
    while start < end:
        yield start
        start += step

def callback(data):

	global mainUrl

	mainUrl = data.data

def callbacktwo(data):

	course = data.data

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

			main()
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

			for link in my_range(0, len(links), 1):
			    
			    if link % 2 != 0:
			 
			    	links2.append(links[link])

			for sublink in links2:
				
				imageNames.append(sublink.split("/")[3])

			pngCount = 0

			jpegCount = 0		
			
			for sublink in links2:
				
				requestLink = mainUrl + sublink

				counter = counter + 1

				imageName = imageNames[counter]


				if "png" in imageName:

					#after having parsed the html that the server returned
					# this generates as many requests as links the server provides
					#and saves the images to ~/output/images/pngs/
					
					time.sleep(3)

					r = requests.get(requestLink, stream = True)

					path = os.path.join(os.path.expanduser('~'), 'output', 'images', 'pngs/')
					
					with open(path+imageName,'wb') as out_file:
					
						shutil.copyfileobj(r.raw, out_file)
					
					del r

					pngCount = pngCount + 1

				else:

					#after having parsed the html that the server returned
					# this generates as many requests as links the server provides
					#and saves the images to ~/output/images/jpegs/
					
					time.sleep(3)

					r = requests.get(requestLink, stream = True)

					path = os.path.join(os.path.expanduser('~'), 'output', 'images', 'jpegs/')
					
					with open(path+imageName,'wb') as out_file:
					
						shutil.copyfileobj(r.raw, out_file)
					
					del r

					jpegCount = jpegCount + 1
					

			status_pub = rospy.Publisher('server_images_info', String, queue_size=10)
				

			rate = rospy.Rate(1)
			
			while not rospy.is_shutdown():

				data = "JPEGS:%d PNGS:%d" %(jpegCount, pngCount)

				rospy.loginfo(data) 
				
				status_pub.publish(data) 
				
				rate.sleep()	
		else:
			
			raise rospy.ServiceException("Bad Request")		

	except rospy.ServiceException:
		pass		


def main():
	
	rospy.init_node('nodroneimagegetter')	

	#no drone challege, where we receive an image list
	# in html and each request needs to be done separately
	# and we have to process and identify one of them

	###### TOPIC SUBSCRIPTION #######

	
	rospy.Subscriber('main_server_url', String, callback) 

	# node to publish the current course

	rospy.Subscriber('course_code', String, callbacktwo)

	rospy.spin()	

if __name__ == '__main__':

	try:
	
		main()

	except (rospy.ROSInterruptException, rospy.ServiceException) as e:
		pass	

