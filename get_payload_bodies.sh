#!/usr/bin/env bash

cat /tmp/jwtsecret | xxd -r -p > /tmp/jwtsecret_bin
JWT=$(jwt encode --secret @/tmp/jwtsecret_bin)

curl \
    --location \
    --request POST 'http://localhost:8551/' \
    --header 'Content-Type: application/json' \
    --header "Authorization: Bearer $JWT" \
    --data-raw "{
        \"jsonrpc\": \"2.0\",
        \"method\": \"engine_getPayloadBodiesV1\",
        \"params\": [[\"$1\"]],
        \"id\": 1
    }"
