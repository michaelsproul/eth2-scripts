#!/usr/bin/env bash

source $(eth2_scripts_dir.sh)/setup.sh

curl "$BEACON_NODE/eth/v1/beacon/states/head/validators" \
    | jq -r '.data | map(select(.validator.slashed == true) | .index) | join("\n")'
