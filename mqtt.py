from umqtt.simple import MQTTClient
import time

class ServoStatusRequest:
    def __init__(self):
        self.mqtt_url = 'mqtt.thingspeak.com'
        self.write_api = '6AXCGP0YJN2QUFEQ'
        self.read_api = 'UTOB3C6YT3AZMEZN'
        self.current_status_topic = 'channels/1001649/publish/{}'.format(self.write_api)
        self.requested_status_topic = 'channels/1001649/subscribe/fields/field2/{}'.format(self.read_api)

    def modify_servo_pos(self, topic, message):
        print(message)
    #     Add code to modify servo pos. according to request and then update servo status

    def MQTT_subscribe_to_request(self):
        self.check_messages = True
        client = MQTTClient(self.mqtt_url)
        client.set_callback(self.modify_servo_pos)
        client.connect(self.requested_status_topic)
        while self.check_messages:
            client.check_msg()
            time.sleep(5)
        client.disconnect()

    def MQTT_publish(self, value):
        client = MQTTClient('esp_mqtt', self.mqtt_url)
        client.connect()
        client.publish(self.current_status_topic.encode(), 'field1={}'.format(str(value)).encode())
        client.disconnect()