#!/bin/bash

init_prod_env_file() {
    local_mode='prod'
    cat <<EOF >$location/.env
MODE=$local_mode

CERT_FILE=cert.pem
KEY_FILE=privkey.pem

# Customize as needed
APP_HOST=
APP_PORT=
SECRET_KEY=
APP_URL_PREFIX=/api

# This path should conform with the path that is provided by uwsgi.ini"
SWAGGER_BASE_URL=

WEBAPI_DOMAIN=https://tobias-blaufuss.de
WEBAPI_PORT=65291
SSL_CA_BUNDLE='/etc/ssl/certs/ca-certificates.crt'
EOF
}

init_dev_env_file() {
    local_mode='dev'
    cat <<EOF >$location/.env
MODE=$local_mode

# Should be empty in $local_mode environment
CERT_FILE=
KEY_FILE=

# Customize as needed
APP_HOST=localhost
APP_PORT=5000
SECRET_KEY=XLrIjHvKsQskA7m
APP_URL_PREFIX=/api

# Should be empty in $local_mode environment
SWAGGER_BASE_URL=

WEBAPI_DOMAIN=https://tobias-blaufuss.de
WEBAPI_PORT=65291
SSL_CA_BUNDLE='/etc/ssl/certs/ca-certificates.crt'
EOF
}

mode=$1
location=$2

# SCRIPT

if [[ -z "$mode" ]]; then
    echo "Provide one of these modes as first parameter: dev, prod"
    exit 1
fi

if [[ ! -d "$location" ]]; then
    echo "Provide a valid destination directory for generating the .env file as second parameter."
    exit 2
fi

echo "Selected mode: $mode"
echo "Destination directory: $location"

if [[ "$mode" = "prod" ]]; then
    init_prod_env_file "$location"
elif [[ "$mode" = "dev" ]]; then
    init_dev_env_file "$location"
else
    echo "Unknown mode: $mode"
    exit 1
fi