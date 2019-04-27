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

#############################
## Configured in balena.io ##
# SECRET_KEY=               #
# APP_URL_PREFIX=           #
#############################

# Should be empty in $local_mode environment
SWAGGER_BASE_URL=""

#############################
## Configured in balena.io ##
# WEBAPI_DOMAIN=            #
# WEBAPI_PORT=              #
#############################

SSL_CA_BUNDLE='/etc/ssl/certs/ca-certificates.crt'
EOF
fi

modprobe i2c-dev
python -u app.py
