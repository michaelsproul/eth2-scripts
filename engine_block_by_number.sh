#!/usr/bin/env bash

set -eo pipefail

if [ $# -le 1 ]
then
    echo "no block number or JWT secret provided"
    echo "usage: ./engine_block_by_numer.sh N JWT [URL]"
    exit 1
fi

block_number=$1

jwtsecret=$2
tmpfile=./.engine_block_by_number_sh_jwt

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
        \"method\": \"eth_getBlockByNumber\",
        \"params\": [\"$block_number\", true],
        \"id\": 1
    }"

rm -f $tmpfile
