#!/usr/bin/env bash

curl -s "http://localhost:5052/eth/v1/beacon/states/head/validators" \
    | jq -r '.data | map(select(.validator.slashed == true) | .index) | join("\n")'
