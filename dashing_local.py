#!/usr/bin/env python

import sys, os, random, time
from amazon_credentials import *
from amazon.api import AmazonAPI
from  inception_predict import *
import socket
import io
import pygame

try:
	# Python2
	from urllib2 import urlopen
except ImportError:
	# Python3
	from urllib.request import urlopen

SCREEN_WIDTH = 800
IMG_MAX_WIDHT = SCREEN_WIDTH/2.0
SCREEN_HEIGHT = 600
IMG_MAX_HEIGHT = SCREEN_HEIGHT/2.0

# Use two contants for clearity
IDLE = 0
GETIMAGES = 1
SHOWING = 2

# Initiate Pygame
pygame.init()
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
idlefont = pygame.font.SysFont("Tg", 50)
keywordfont = pygame.font.SysFont("Tg", 40)
searchingfont = pygame.font.SysFont("Tg", 30)
productfont = pygame.font.SysFont("Tg", 30)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),  pygame.RESIZABLE )
screen.fill((255, 255, 255))
pygame.display.flip()

# Location of the images we want to have analyzed
# img_folder = "/home/pi/jasper/img/kendalljenner"
img_folder = "/home/javl/tmp/mxnet/img/kendalljenner"

# Socket for sending UDP data to our Processing sketch on a different machine (RPi)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # needed to be able to broadcast


# Setup our Amazon API. Credentials are loaded from amazon_credentials.py
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

status = IDLE

def drawKeyword(_keyword):
	keyword_text = keywordfont.render(_keyword, 1, (255, 255, 255))
	rect = keyword_text.get_rect(center=(SCREEN_WIDTH/2, 50))
	pygame.draw.rect(screen, (0, 0, 0), (rect.x-10, rect.y+2, rect.w+20, rect.h))
	screen.blit(keyword_text, rect)
	pygame.display.flip()

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=True, bkg=None):
	rect = pygame.Rect(rect)
	y = rect.top
	print "y is ", y
	lineSpacing = -2

	# get the height of the font
	fontHeight = font.size("Tg")[1]

	while text:
		i = 1

		# determine if the row of text will be outside our area
		if y + fontHeight > rect.bottom:
			break

		# determine maximum width of line
		while font.size(text[:i])[0] < rect.width and i < len(text):
			i += 1

		# if we've wrapped the text, then adjust the wrap to the last word
		if i < len(text):
			i = text.rfind(" ", 0, i) + 1

		# render the line and blit it to the surface
		if bkg:
			image = font.render(text[:i], 1, color, bkg)
			image.set_colorkey(bkg)
		else:
			image = font.render(text[:i], aa, color)
		rect = image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-80))
		pygame.draw.rect(screen, (0, 0, 0), (rect.x-10, rect.y+14, rect.w+20, rect.h+4))

		surface.blit(image, (rect.left, y))
		y += fontHeight + lineSpacing

		# remove the text we just blitted
		text = text[i:]

	return text

# Keep looping
while True:

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit(); #sys.exit() if sys is imported
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if status == IDLE:
						status = GETIMAGES
				elif event.key == pygame.K_ESCAPE:
					pygame.quit()

	if status == IDLE:

		# render text
		idle_text = idlefont.render("Press Dashing button to search and order...", True, (0,0,0))
		idle_text_rect = idle_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
		screen.blit(idle_text, idle_text_rect)
		pygame.display.flip()

	elif status == GETIMAGES:
		screen.fill((255, 255, 255))

		# get a random imag efrom our folder and load it into our pygame image
		src_image = random.choice(os.listdir(img_folder))
		img = pygame.image.load("{img_folder}/{filename}".format(img_folder=img_folder, filename=src_image))
		# the the size of the image and calculate how much we need to scale it to fit half of the screen
		img_rect = img.get_rect()
		scale = min( (float(SCREEN_WIDTH)/2.0)/float(img_rect.w), float(SCREEN_HEIGHT)/float(img_rect.h))
		img = pygame.transform.scale(img, (int(img_rect.w*scale), int(img_rect.h*scale)))
		# center the image on the y axis
		img_rect = img.get_rect()
		screen.blit(img, (0, (SCREEN_HEIGHT-img_rect.h)/2.0))
		pygame.display.flip()

		# Analyze the image using MXNet, and just jump to the next loop of an error occurs
		try:
			result = predict_from_local_file("{}/{}".format(img_folder, src_image), 1)
		except Exception, e:
			continue;

		# Get the keywords found, and jump to the next loop of there was none
		try:
			keyword = result[0][1][10:]

			drawKeyword(keyword)

		except: # no keyword found
			continue

		searching_text = searchingfont.render("Searching for", 1, (0, 0, 0))
		rect = searching_text.get_rect(center=(SCREEN_WIDTH*0.75, SCREEN_HEIGHT/2.0 - 30))
		screen.blit(searching_text, rect)

		searching_text = searchingfont.render("matching products", 1, (0, 0, 0))
		rect = searching_text.get_rect(center=(SCREEN_WIDTH*0.75, SCREEN_HEIGHT/2.0))
		screen.blit(searching_text, rect)

		searching_text = searchingfont.render("on Amazon...", 1, (0, 0, 0))
		rect = searching_text.get_rect(center=(SCREEN_WIDTH*0.75, SCREEN_HEIGHT/2.0 + 30))
		screen.blit(searching_text, rect)

		pygame.display.flip()

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
			drawText(screen, product.title, (255, 255, 255), (20, SCREEN_HEIGHT-80, SCREEN_WIDTH -40, SCREEN_HEIGHT), keywordfont, aa=False, bkg=None)
			pygame.display.flip()


		except Exception, e:
			print "Error during lookup: ", e
			continue

		# Load an image from the large_image_url
		print "get img: ", product.large_image_url
		image_str = urlopen(product.large_image_url).read()
		a = time.time()
		img = pygame.image.load(io.BytesIO(image_str))
		# the the size of the image and calculate how much we need to scale it to fit half of the screen
		img_rect = img.get_rect()
		scale = min( (float(SCREEN_WIDTH)/2.0)/float(img_rect.w), float(SCREEN_HEIGHT)/float(img_rect.h))
		img = pygame.transform.scale(img, (int(img_rect.w*scale), int(img_rect.h*scale)))
		# center the image on the y axis
		img_rect = img.get_rect()
		screen.blit(img, (SCREEN_WIDTH/2.0, (SCREEN_HEIGHT-img_rect.h)/2.0))
		drawText(screen, product.title, (255, 255, 255), (20, SCREEN_HEIGHT-80, SCREEN_WIDTH -40, SCREEN_HEIGHT), keywordfont, aa=False, bkg=None)

		# draw keyword on top
		drawKeyword(keyword)
		pygame.display.flip()

		# Wait for a bit and then reset
		time.sleep(6)
		status = IDLE
		screen.fill((255, 255, 255))
