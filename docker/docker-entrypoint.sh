#!/bin/sh

cd src

env_file=".env"
if [ ! -e "$env_file" ]
then
        cat <<EOF >$env_file
MODE=prod

# Should be empty in $local_mode environment
CERT_FILE=""
KEY_FILE=""

# Customize as needed
APP_HOST=0.0.0.0
APP_PORT=80
SECRET_KEY=XLrIjHvKsQskA7m
APP_URL_PREFIX=/api

# Should be empty in $local_mode environment
SWAGGER_BASE_URL=""

WEBAPI_DOMAIN=https://contabo.tobias-blaufuss.de
WEBAPI_PORT=60001
SSL_CA_BUNDLE='/etc/ssl/certs/ca-certificates.crt'
EOF
fi

modprobe i2c-dev
python -u app.py
