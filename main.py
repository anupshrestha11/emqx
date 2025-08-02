from publisher import Publisher
from subscriber import Subscriber
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MQTT Broker settings
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "localhost")
PORT = int(os.getenv("PORT", 1883))
TOPIC = "emqx/test"

# mTLS settings
CA_CERTS = os.getenv("CA_CERTS")
CERTFILE = os.getenv("CERTFILE")
KEYFILE = os.getenv("KEYFILE")


def main():
    received_messages = []

    def on_message_callback(client, userdata, msg):
        message = msg.payload.decode()
        print(f"Received from {msg.topic}: {message}")
        received_messages.append(message)

    # Create a publisher
    publisher = Publisher(
        BROKER_ADDRESS,
        PORT,
        client_id="publisher",
        ca_certs=CA_CERTS,
        certfile=CERTFILE,
        keyfile=KEYFILE,
    )
    publisher.connect()

    # Create a subscriber
    subscriber = Subscriber(
        BROKER_ADDRESS,
        PORT,
        client_id="subscriber",
        on_message=on_message_callback,
        ca_certs=CA_CERTS,
        certfile=CERTFILE,
        keyfile=KEYFILE,
    )
    subscriber.connect()
    subscriber.subscribe(TOPIC)

    # Start listening in a separate thread
    import threading
    subscriber_thread = threading.Thread(target=subscriber.start_listening)
    subscriber_thread.daemon = True
    subscriber_thread.start()

    # Add a small delay to ensure the subscriber is ready
    time.sleep(1)

    # Publish messages
    sent_messages = []
    for i in range(5):
        message = f"Message {i}"
        publisher.publish(TOPIC, message)
        sent_messages.append(message)
        time.sleep(1)

    # Wait for all messages to be received
    time.sleep(2)

    # Disconnect
    publisher.disconnect()
    subscriber.disconnect()

    # Verification
    print("\n--- Verification ---")
    print(f"Sent messages: {sent_messages}")
    print(f"Received messages: {received_messages}")
    if sent_messages == received_messages:
        print("Success: All messages received correctly.")
    else:
        print("Error: Mismatch in sent and received messages.")


if __name__ == "__main__":
    main()
