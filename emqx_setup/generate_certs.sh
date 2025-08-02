#!/bin/bash

# Create certificates directory
mkdir -p certs
cd certs

# Generate CA private key
openssl genrsa -out ca-key.pem 4096

# Generate CA certificate
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca-cert.pem -subj "/C=US/ST=CA/L=San Francisco/O=MyOrg/OU=MyOrgUnit/CN=MyCA"

# Generate server private key
openssl genrsa -out server-key.pem 4096

# Generate server certificate signing request
openssl req -subj "/C=US/ST=CA/L=San Francisco/O=MyOrg/OU=MyOrgUnit/CN=emqx" -sha256 -new -key server-key.pem -out server.csr

# Create extensions file for server certificate
cat > server-extfile.cnf <<EOF
subjectAltName = DNS:emqx,DNS:localhost,IP:127.0.0.1,IP:172.21.0.2
extendedKeyUsage = serverAuth
EOF

# Generate server certificate
openssl x509 -req -days 365 -in server.csr -CA ca-cert.pem -CAkey ca-key.pem -out server-cert.pem -extfile server-extfile.cnf -CAcreateserial

# Generate client private key
openssl genrsa -out client-key.pem 4096

# Generate client certificate signing request
openssl req -subj "/C=US/ST=CA/L=San Francisco/O=MyOrg/OU=MyOrgUnit/CN=client" -new -key client-key.pem -out client.csr

# Create extensions file for client certificate
cat > client-extfile.cnf <<EOF
extendedKeyUsage = clientAuth
EOF

# Generate client certificate
openssl x509 -req -days 365 -in client.csr -CA ca-cert.pem -CAkey ca-key.pem -out client-cert.pem -extfile client-extfile.cnf -CAcreateserial

# Clean up
rm server.csr client.csr server-extfile.cnf client-extfile.cnf

# Set permissions
chmod 400 ca-key.pem server-key.pem client-key.pem
chmod 444 ca-cert.pem server-cert.pem client-cert.pem

echo "Certificates generated successfully!"
echo "Files created:"
echo "  ca-cert.pem     - Certificate Authority certificate"
echo "  ca-key.pem      - Certificate Authority private key"
echo "  server-cert.pem - Server certificate"
echo "  server-key.pem  - Server private key"
echo "  client-cert.pem - Client certificate"
echo "  client-key.pem  - Client private key"
