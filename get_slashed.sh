#!/usr/bin/env bash

curl -s "http://localhost:5052/beacon/validators/all" \
    | jq -r 'map(select(.validator.slashed == true) | .validator_index) | join("\n")'