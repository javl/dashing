#!/usr/bin/env python
import sys, os, random, time
from amazon_credentials import *
from amazon.api import AmazonAPI
from  inception_predict import *
import socket

# Location of the images we want to have analyzed
img_folder = "/home/pi/jasper/img/kendalljenner"

# Socket for sending UDP data to our Processing sketch on a different machine (RPi)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # needed to be able to broadcast

# To make sure packeges are received I send them multiple times, but each version of the same
# message has the same counter value in its data so the receiver can easily discard messages
# it has already seen
counter = 0

# Setup our Amazon API. Credentials are loaded from amazon_credentials.py
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

# Keep looping
while True:
	counter += 1

	# My DIY dash button will fake a 'return' key.
	user_input = raw_input("Wating for Dash button...")
	if user_input == 'x': # press x to exit
		exit()
	elif user_input == '': # return was pressed

		# get a random imag efrom our folder
		src_image = random.choice(os.listdir(img_folder))

		# Packets always contain 5 values. If a field is not used by a specific action, an 'x' is
		# used for its value
		#
		# [0] 'dash' is used as identifier, so I can asily see what network messages came from mee
		# [1] counter is send to track double messages
		# [2] 'original', 'found' or 'clear' descibe the type of message
		# [3] With 'original' and 'found' this is the path to an image file

		print "sending: dash,{counter},original,{img_folder}/{filename}".format(counter=counter,img_folder=img_folder,filename=src_image)
		s.sendto("dash,{counter},original,{img_folder}/{filename}".format(counter=counter,img_folder=img_folder,filename=src_image), 0, ('192.168.2.255', 6001))
		s.sendto("dash,{counter},original,{img_folder}/{filename}".format(counter=counter,img_folder=img_folder,filename=src_image), 0, ('192.168.2.255', 6001))
		s.sendto("dash,{counter},original,{img_folder}/{filename}".format(counter=counter,img_folder=img_folder,filename=src_image), 0, ('192.168.2.255', 6001))
		s.sendto("dash,{counter},original,{img_folder}/{filename}".format(counter=counter,img_folder=img_folder,filename=src_image), 0, ('192.168.2.255', 6001))
		counter += 1 # increment counter after every set of messages

		# Analyze the image using MXNet, and just jump to the next loop of an error occurs
		try:
			result = predict_from_local_file("{}/{}".format(img_folder, src_image))
		except Exception, e:
			continue;

		# Get the keywords found, and jump to the next loop of there was none
		try:
			keyword = result[0][1].split(' ')[1]
			print "sending: dash,{counter},keyword,{keyword},x".format(counter=counter,keyword=keyword)
			s.sendto("dash,{counter},keyword,{keyword}".format(counter=counter,keyword=keyword), 0, ('192.168.2.255', 6001))
			s.sendto("dash,{counter},keyword,{keyword}".format(counter=counter,keyword=keyword), 0, ('192.168.2.255', 6001))
			s.sendto("dash,{counter},keyword,{keyword}".format(counter=counter,keyword=keyword), 0, ('192.168.2.255', 6001))
			s.sendto("dash,{counter},keyword,{keyword}".format(counter=counter,keyword=keyword), 0, ('192.168.2.255', 6001))
			counter += 1
		except: # no keyword found
			continue

		# Try finding a product using our keyword, and jump to the next loop of there was none
		try:
			products = amazon.search_n(1, Keywords=keyword, SearchIndex='All')
			print products[0].asin
		except Exception, e:
			print e
			continue

		# Lookup info of our product, and jump to the next loop of there was none
		try:
			product = amazon.lookup(ItemId=products[0].asin)
			if product.large_image_url == None:
				continue
		except Exception, e:
			print "error lookup"
			print e
			continue

		# Tell our receiver about the found image
		print "sending: dash,{counter},found,{img_url}".format(counter=counter, img_url=product.large_image_url)
		s.sendto("dash,{counter},found,{img_url}".format(counter=counter, img_url=product.large_image_url), 0, ('192.168.2.255', 6001))
		s.sendto("dash,{counter},found,{img_url}".format(counter=counter, img_url=product.large_image_url), 0, ('192.168.2.255', 6001))
		s.sendto("dash,{counter},found,{img_url}".format(counter=counter, img_url=product.large_image_url), 0, ('192.168.2.255', 6001))
		s.sendto("dash,{counter},found,{img_url}".format(counter=counter, img_url=product.large_image_url), 0, ('192.168.2.255', 6001))
		counter += 1

		# Wait for a bit and then reset
		print "Waiting 6 seconds"
		time.sleep(6)

		print "sending: dash,{counter},clear,x".format(counter=counter)
		s.sendto("dash,{counter},clear,x".format(counter=counter), 0, ('192.168.2.255', 6001))
		s.sendto("dash,{counter},clear,x".format(counter=counter), 0, ('192.168.2.255', 6001))
		s.sendto("dash,{counter},clear,x".format(counter=counter), 0, ('192.168.2.255', 6001))
		s.sendto("dash,{counter},clear,x".format(counter=counter), 0, ('192.168.2.255', 6001))
		counter += 1