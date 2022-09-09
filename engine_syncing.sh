#!/usr/bin/env bash

set -eo pipefail

if [ $# -eq 0 ]
then
    echo "no JWT secret provided"
    echo "usage: ./engine_syncing.sh JWT [URL]"
    exit 1
fi

jwtsecret=$1
tmpfile=./.engine_syncing_sh_jwt

engine_url=$2
engine_url=${engine_url:="http://localhost:8551"}

cat $jwtsecret | xxd -r -p > $tmpfile
JWT=$(jwt encode --secret @$tmpfile)

curl \
    --location \
    --request POST $engine_url \
    --header 'Content-Type: application/json' \
    --header "Authorization: Bearer $JWT" \
    --data-raw "{
        \"jsonrpc\": \"2.0\",
        \"method\": \"eth_syncing\",
        \"params\": [],
        \"id\": 1
    }"

rm -f $tmpfile
