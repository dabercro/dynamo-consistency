#! /bin/bash

which dynamo || exit 0

/etc/pki/tls/certs/make-dummy-cert /etc/pki/tls/certs/localhost.crt
chmod +r /etc/pki/tls/certs/localhost.crt
# Create a certificate for dynamo user
printf "US\nMass\nBahston\nDynamo\ntest\nlocalhost\n\n" | \
    openssl req -new -newkey rsa:1024 -days 365 -nodes -x509 -keyout /tmp/x509up_u500 -out /tmp/x509up_u500
chown dynamo:dynamo /tmp/x509up_u500
# Add certificates to trusted
cp /tmp/x509up_u500 /etc/pki/tls/certs/localhost.crt /etc/pki/ca-trust/source/anchors/
update-ca-trust extract

cp /tmp/x509up_u500 /tmp/x509up_u0

yes | dynamo-user-auth --user dynamo --dn "/C=US/ST=Mass/L=Bahston/O=Dynamo/OU=test/CN=localhost" --role admin
dynamo-user-auth --user dynamo --role admin --target inventory
