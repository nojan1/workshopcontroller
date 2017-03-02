""" Configuration values for application """

MQTT_CLIENTID = "Workshop enviromental control unit"
MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883

#For servo control
SERVO_I2C_ADDRESS = 0x40
SERVO_I2C_BUSNUM = 1

#What is the max and min heating values the servos can manage
HEAT_MAX = 24
HEAT_MIN = 10

#Should a fake heating controler be used
FAKE_MODE = True