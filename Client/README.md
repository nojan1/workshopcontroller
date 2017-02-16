Client
======

The scripts running on the client.

# Entrypoints

 * **submit_temperatures.py** Run by cron to periodically submit temperatures from the 1-wire temp sensors to MQTT server.
 * **order_listener.py** Run in background to control thermostat servos based on orders on a MQTT topic.

# MQTT - Topics

**/workshop/temperature/[SERIALNUMBER]** temperature reading from sensors are published here. The serialnumber is the serial of the temp sensor.

**/workshop/heating/setting** This topic is monitored and the heating is set to the value published here in the format of *[UPSTAIRS];[DOWNSTAIRS]*, where values are degrees in celsius.