# EMQX Publisher/Subscriber with Python

This project provides a simple yet powerful demonstration of the publisher-subscriber pattern using the EMQX MQTT broker. It includes Python classes for a publisher and a subscriber, a main script to orchestrate the communication, and a Docker Compose setup for running the EMQX broker locally.

## Features

- **Publisher/Subscriber Classes:** Modular and reusable classes for MQTT publishing and subscribing.
- **EMQX Docker Integration:** Easily start and stop a local EMQX broker using Docker Compose.
- **Secure Communication:** Supports MQTT over TLS with mutual authentication (mTLS) for secure connections to remote brokers.
- **Configuration Management:** Uses a `.env` file to manage connection settings and certificate paths, keeping sensitive information out of the code.
- **Verification Logic:** Includes a verification step in the main script to confirm that all published messages are successfully received by the subscriber.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Configuration

Configuration for the MQTT broker is managed through the `.env` file.

### For Local Development

For connecting to the local EMQX broker, your `.env` file can be left with default or empty values, as the scripts default to `localhost:1883`.

### For Remote (mTLS) Connection

To connect to a secure remote broker, create or update the `.env` file with your broker's details and the paths to your TLS certificates:

```
BROKER_ADDRESS=your_remote_broker_address
PORT=8883
CA_CERTS=path/to/your/ca.crt
CERTFILE=path/to/your/client.crt
KEYFILE=path/to/your/client.key
```

Remember to install the `python-dotenv` package to load these variables:
`pip install python-dotenv`

## Usage

1.  **Start the EMQX Broker:**
    Open a terminal and run the following command to start the EMQX broker in the background:
    ```bash
    docker compose up -d
    ```

2.  **Run the Application:**
    In another terminal, run the main script to see the publisher and subscriber in action:
    ```bash
    python3 main.py
    ```
    The script will publish several messages and then print a verification section to confirm that all messages were received.

3.  **Stop the EMQX Broker:**
    When you are finished, you can stop the broker with:
    ```bash
    docker compose down
    ```

## File Structure

- `publisher.py`: Contains the `Publisher` class for connecting and publishing messages.
- `subscriber.py`: Contains the `Subscriber` class for connecting, subscribing, and receiving messages.
- `main.py`: The main entry point of the application. It initializes the publisher and subscriber, runs the test, and verifies the results.
- `docker-compose.yaml`: Defines the EMQX service for local testing.
- `.env`: Stores configuration variables (ignored by Git).
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `requirements.txt`: Lists the Python dependencies for the project.
- `README.md`: This file.
