
# Jack Carter
"""
 This file will be on the R-pi, and will contact the Sound Sensor
 1. Establish Publish
 2. while loop of detecting sound sensor - collect 1000 samples
    run moving average
 3. If triggered, publish
 4. Go back to loop
"""

""" Initializes the GrovePi """
import time
import grovepi

""" Initializes the MQTT """
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	print("Connected t server (i.e.,broker) with result code "+str(rc))

def on_message(client, userdata, msg):
	print( "on_message: " + msg.topic + " " + str(msg.payload, 'utf-8'))

#I chose to have threshold be accessable as a global variable, this way it can be changed easily if you desire your library to be below different volume thresholds
threshold = 300

#initialize port of sound sensor
sound_sensor_port = 0
grovepi.pinMode(sound_sensor_port,"INPUT")

"""
This next section will be the sensing portion
"""

#this section is covered in publisher_and_subscriber_example.py
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
client.loop_start()


sensor_value = 0
moving_average_total = 0
cycle_average = 0
avg_count = 0

"""
I implement an average of 1000 samples because occasionally a single reading might be read incorrect and that could meet the threshold
and send an alert falsely
"""

while True:
	try:
		sensor_value = grovepi.analogRead(sound_sensor_port)
		moving_average_total = sensor_value + moving_average_total
		if avg_count >= 1000:
			print("end of cycle: total = %d" %moving_average_total, "average = %d " % (moving_average_total / avg_count))
			if (moving_average_total / avg_count) > threshold:
				print("Too Loud!")
				client.publish('jackcart/sound_sensor','Noise Alert')
			avg_count = 0
			moving_average_total = 0
		else:
			avg_count = avg_count + 1

		#this is more for debuggin and assurance, so that the publisher knows the sensor is working properly
			if (avg_count % 25) == 0:
				print("Counting %d - " %avg_count, "Sensing %d" %sensor_value)

		#add a delay, this way you can save energy and still get enough information to know the volume of the surroundings
		time.sleep(.001)
	except IOError:
		print ("Error")
