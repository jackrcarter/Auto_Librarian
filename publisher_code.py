
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
while True:
	try:
		sensor_value = grovepi.analogRead(sound_sensor_port)
		moving_average_total = sensor_value + moving_average_total
		if avg_count >= 1000:
			print("end of cycle: total = %d" %moving_average_total, "average = %d " % (moving_average_total / avg_count))
			if (moving_average_total / avg_count) > 225:
				print("Too Loud!")
				client.publish('jackcart/sound_sensor','Noise Alert')
			avg_count = 0
			moving_average_total = 0
		else:
			avg_count = avg_count + 1
			if (avg_count % 5) == 0:
				print("Counting %d - " %avg_count, "Sensing %d" %sensor_value)
		time.sleep(.001)
	except IOError:
		print ("Error")
