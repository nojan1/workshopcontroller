""" Configuration values for application """

MQTT_CLIENTID = "Workshop enviromental control unit"
MQTT_HOST = "127.0.0.1"
MQTT_PORT = 7000 #1883

SERVO_I2C_ADDRESS = 0x41
SERVO_I2C_BUSNUM = 2

HEAT_MAX = 24
HEAT_MIN = 10

FAKE_MODE = True