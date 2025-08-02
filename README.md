# EMQX Publisher/Subscriber with Python - mTLS Ready

This project provides a comprehensive demonstration of the publisher-subscriber pattern using the EMQX MQTT broker with support for both local development and secure mTLS (mutual TLS) connections. It includes Python classes for publisher and subscriber, Docker Compose setup, and automated certificate generation for secure connections.

## ✅ Features

- **Publisher/Subscriber Classes:** Modular and reusable classes for MQTT publishing and subscribing
- **EMQX Docker Integration:** Complete Docker Compose setup with mTLS support
- **Secure mTLS Communication:** Mutual TLS authentication with auto-generated certificates
- **Environment Configuration:** Uses `.env` file for flexible configuration management
- **Verification Logic:** Built-in verification to confirm message delivery
- **Dashboard Access:** EMQX web dashboard for monitoring and management
- **Connection Testing:** Dedicated mTLS connection test script

## ✅ What's Working

- ✅ EMQX container running with mTLS enabled on port 8883
- ✅ SSL/TLS certificates auto-generated and properly configured
- ✅ Python MQTT clients with mTLS support
- ✅ Environment variables configuration via `.env` file
- ✅ EMQX Dashboard accessible at http://localhost:18083
- ✅ Successful mTLS connection verification

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)
- OpenSSL (for certificate generation - usually pre-installed on Linux/macOS)

## Quick Start (mTLS Mode)

1. **Start EMQX with mTLS**
   ```bash
   docker compose up -d
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test mTLS Connection**
   ```bash
   python test_mtls.py
   ```
   Expected output: `✅ mTLS connection successful!`

4. **Run the MQTT Publisher/Subscriber**
   ```bash
   python main.py
   ```

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Start EMQX with mTLS (recommended):**
   ```bash
   docker compose up -d
   ```

## Configuration

### Environment Variables (.env)

The project uses a `.env` file for configuration. The current setup is configured for mTLS:

```env
# EMQX MQTT Broker Configuration with mTLS
BROKER_ADDRESS=localhost
PORT=8883

# mTLS Certificate Configuration
CA_CERTS=./emqx_setup/certs/ca-cert.pem
CERTFILE=./emqx_setup/certs/client-cert.pem
KEYFILE=./emqx_setup/certs/client-key.pem

# EMQX Dashboard Configuration
DASHBOARD_PORT=18083
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=public
```

### For Local Development (Non-TLS)

To use standard MQTT without TLS, update your `.env` file:

```env
BROKER_ADDRESS=localhost
PORT=1883
# Comment out or remove certificate paths
# CA_CERTS=
# CERTFILE=
# KEYFILE=
```

### EMQX Dashboard

- **URL**: http://localhost:18083
- **Username**: admin
- **Password**: public

## Certificate Management

### Auto-Generated Certificates

Certificates are automatically generated and located in `emqx_setup/certs/`:

- `ca-cert.pem`: Certificate Authority certificate
- `ca-key.pem`: Certificate Authority private key
- `server-cert.pem`: Server certificate for EMQX
- `server-key.pem`: Server private key for EMQX
- `client-cert.pem`: Client certificate for MQTT clients
- `client-key.pem`: Client private key for MQTT clients

### Regenerating Certificates

If you need to regenerate certificates:

```bash
cd emqx_setup
./generate_certs.sh
```

## Usage

### Standard Workflow

1. **Start the EMQX Broker:**
   ```bash
   docker compose up -d
   ```

2. **Verify mTLS Connection:**
   ```bash
   python test_mtls.py
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```
   The script will publish several messages and verify that all messages were received.

4. **Stop the EMQX Broker:**
   ```bash
   docker compose down
   ```

### Verification Steps

1. **Container Status**: `docker ps` should show `emqx_container` as `Up`
2. **mTLS Test**: `python test_mtls.py` should show successful connection
3. **MQTT Communication**: `python main.py` should show message exchange
4. **Dashboard Access**: http://localhost:18083 should be accessible

## Key Features

### mTLS Configuration
- **Port 8883**: Secure MQTT with mutual TLS authentication
- **Client verification**: Requires valid client certificates
- **CA validation**: All certificates validated against the CA

### Docker Configuration
- Simplified environment variable configuration
- WSS listener disabled to avoid certificate conflicts
- Persistent data and log volumes
- Network isolation with custom bridge network

## File Structure

```
├── docker-compose.yaml           # Docker Compose with mTLS config
├── .env                         # Environment variables
├── main.py                      # Main MQTT client application
├── publisher.py                 # MQTT Publisher class with mTLS
├── subscriber.py                # MQTT Subscriber class with mTLS
├── test_mtls.py                # mTLS connection test script
├── requirements.txt             # Python dependencies
├── README.md                   # This documentation
├── emqx_setup/
│   ├── generate_certs.sh       # Certificate generation script
│   ├── emqx.conf              # EMQX configuration file
│   └── certs/                 # SSL certificates (generated)
│       ├── ca-cert.pem        # CA certificate
│       ├── ca-key.pem         # CA private key
│       ├── server-cert.pem    # Server certificate
│       ├── server-key.pem     # Server private key
│       ├── client-cert.pem    # Client certificate
│       └── client-key.pem     # Client private key
└── docker_vol/                # Docker volumes for EMQX data and logs
```

## Security Notes

- All private keys are protected with restricted file permissions
- Client certificates are required for all mTLS connections
- Dashboard uses default credentials (change in production)
- WSS (WebSocket Secure) is disabled to focus on MQTT mTLS
- Never commit private keys to version control

## Troubleshooting

### Common Issues

- **Container restarting**: Check `docker logs emqx_container`
- **Certificate errors**: Verify certificate files exist in `emqx_setup/certs/`
- **Connection refused**: Ensure container is running with `docker ps`
- **Permission denied**: Check certificate file permissions
- **mTLS connection fails**: Run `python test_mtls.py` for detailed error info

### For Remote mTLS Connections

If connecting to a remote broker with your own certificates:

```env
BROKER_ADDRESS=your_remote_broker_address
PORT=8883
CA_CERTS=path/to/your/ca.crt
CERTFILE=path/to/your/client.crt
KEYFILE=path/to/your/client.key
```

## Development Notes

The project is designed to work seamlessly with both local development (using the included Docker setup) and production environments with proper mTLS configuration. The modular design allows easy switching between secure and non-secure connections through environment variables.
