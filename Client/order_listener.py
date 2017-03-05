import paho.mqtt.client as mqtt
import config
import traceback

from dummy_heat_controller import *

if config.FAKE_MODE == False:
    from servo_heat_controller import *

class Worker(object):
    def __init__(self):
        self.client = mqtt.Client(client_id=config.MQTT_CLIENTID)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        if config.FAKE_MODE:
            self.heat_controller = DummyHeatController()
        else:
            self.heat_controller = ServoHeatController()
        
    def run(self):
        self.client.connect(config.MQTT_HOST, config.MQTT_PORT, 60)
        self.client.loop_forever()

    def on_connect(self, client_arg, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        self.client.subscribe("/workshop/heating/setting")

    def on_message(self, client_arg, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        try:
            parts = msg.payload.decode('ascii').split(";")
            downstairs, upstairs = self.heat_controller.set_heat(float(parts[0]), float(parts[1]))

            self.client.publish("/workshop/heating/confirmation", str(downstairs) + ";" + str(upstairs))
        except Exception as e:
            print("Error ocurred handling set request: '{0}'".format(e))
            traceback.print_exc()


if __name__ == "__main__":
    try:
        Worker().run()
    except KeyboardInterrupt:
        pass
