from publisher import Publisher
from subscriber import Subscriber
import time

BROKER_ADDRESS = "localhost"
PORT = 1883
TOPIC = "emqx/test"

def main():
    received_messages = []

    # Create a publisher
    publisher = Publisher(BROKER_ADDRESS, PORT, client_id="publisher")
    publisher.connect()

    # Create a subscriber
    subscriber = Subscriber(BROKER_ADDRESS, PORT, client_id="subscriber")
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