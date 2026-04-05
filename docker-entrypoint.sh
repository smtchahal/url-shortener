#!/bin/sh
set -eu

if [ ! -f /run/secrets/secret_key ]; then
    echo "ERROR: Mount a Docker secret at /run/secrets/secret_key" >&2
    exit 1
fi

SECRET_KEY=$(cat /run/secrets/secret_key)
export SECRET_KEY

exec "$@"
