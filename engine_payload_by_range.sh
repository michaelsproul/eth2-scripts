#!/usr/bin/env bash

set -eo pipefail

if [ $# -le 1 ]
then
    echo "no block number or JWT secret provided"
    echo "usage: ./engine_payload_by_range.sh N JWT [URL]"
    exit 1
fi

block_number=$1

jwtsecret=$2
tmpfile=./.engine_payload_by_range_sh_jwt

engine_url=$3
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
        \"method\": \"engine_getPayloadBodiesByRangeV1\",
        \"params\": [\"$block_number\", \"0x1\"],
        \"id\": 1
    }"

rm -f $tmpfile
