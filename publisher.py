import paho.mqtt.client as mqtt
import ssl
import time

class Publisher:
    def __init__(self, broker_address, port, client_id="", ca_certs=None, certfile=None, keyfile=None):
        self.broker_address = broker_address
        self.port = port
        self.client_id = client_id
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect

        self.ca_certs = ca_certs
        self.certfile = certfile
        self.keyfile = keyfile

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker!: {self.client_id}")
        else:
            print(f"Failed to connect, return code {rc}\n: {self.client_id}")

    def connect(self):
        if self.ca_certs:
            self.client.tls_set(
                ca_certs=self.ca_certs,
                certfile=self.certfile,
                keyfile=self.keyfile,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS
            )
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_start()

    def publish(self, topic, payload):
        self.client.publish(topic, payload)
        print(f"Publisher ::: Published to {topic}: {payload}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()