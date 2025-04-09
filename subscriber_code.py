"""
 This file will be on the client node, and will
 1. Establish subscription to R-pi
 2. Wait for publisher to publish a volume alert
 3. once alert is published, mark flag
 4. if flag, summon the librarian
"""


import paho.mqtt.client as mqtt
import time
from playsound import playsound
from PIL import Image
import random , os

def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))
	#subscribe to the sound sensor topic here
	client.subscribe('jackcart/sound_sensor')
	client.message_callback_add('jackcart/sound_sensor', sound_sensor_callback)

def on_message(client, userdata, msg):
	pass

def sound_sensor_callback(client, userdata, msg):
	print(str(msg.payload, 'utf-8'))

	#randomly chooses if monster footsteps will be played (because librarians are big scary monsters that patrol libraries)
	n=random.randint(0,30)
	if (n % 2) == 0:
		playsound('Monster-Footsteps-B-www.fesliyanstudios.com.mp3')

	#randomly chooses a file from the collection of angry librarian photos to display
	path =r'/home/ee250/Final_project_client/images'
	random_filename = random.choice([
        	x for x in os.listdir(path)
        	if os.path.isfile(os.path.join(path, x))
	])
	with Image.open('/home/ee250/Final_project_client/images/%s' %random_filename) as img:
                img.show()
	#plays the iconic librarian noise.... shushing
	playsound("Person-Saying-Shh-Quick-A-www.fesliyanstudios.com.mp3")

# esablishes the link to the MQTT server
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host = "eclipse.usc.edu", port = 11000, keepalive=60)
client.loop_start()

#runs forever
while True:
	time.sleep(1)