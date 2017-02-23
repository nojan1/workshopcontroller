#!/usr/bin/python

#
# Requirments:
#  dtoverlay=w1-gpio  in /boot/config.txt
#   
#  w1-gpio and w1-therm modules loaded
#

import os
import time
import config
import paho.mqtt.client as mqtt

DEVICE_PATH = "/sys/bus/w1/devices"

def read_temp_raw(device_file_arg):
    f = open(device_file_arg, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file_arg):
    lines = read_temp_raw(device_file_arg)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file_arg)
        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0

    return temp_c

client = mqtt.Client(client_id=config.MQTT_CLIENTID)
client.connect(config.MQTT_HOST, config.MQTT_PORT, 60)

for device_folder in os.listdir(DEVICE_PATH):
    if device_folder.startswith("28"):
        device_file = os.path.join(device_folder, "/w1_slave")
        if os.path.exists(device_file):
            temp = read_temp(device_file)
            client.publish("/workshop/temperature/" + device_folder, temp, 0)

client.disconnect()
