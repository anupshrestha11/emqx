import paho.mqtt.client as mqtt
import ssl

class Subscriber:
    def __init__(self, broker_address, port, client_id="", on_message=None, ca_certs=None, certfile=None, keyfile=None):
        self.broker_address = broker_address
        self.port = port
        self.client_id = client_id
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        if on_message:
            self.client.on_message = on_message
        else:
            self.client.on_message = self.on_message

        self.ca_certs = ca_certs
        self.certfile = certfile
        self.keyfile = keyfile

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

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

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print(f"Subscribed to {topic}")

    def on_message(self, client, userdata, msg):
        print(f"Subscriber ::: Received from {msg.topic}: {msg.payload.decode()}")

    def start_listening(self):
        self.client.loop_forever()

    def disconnect(self):
        self.client.disconnect()