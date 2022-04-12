#!/usr/bin/env bash

curl \
    --location \
    --request POST 'http://localhost:8545/' \
    --header 'Content-Type: application/json' \
    --data-raw "{
        \"jsonrpc\": \"2.0\",
        \"method\": \"eth_getBlockByHash\",
        \"params\": [\"$1\", true],
        \"id\": 1
    }"
