#!/usr/bin/env bash

source $(eth2_scripts_dir.sh)/setup.sh

curl -H "Accept: application/octet-stream" "$BEACON_NODE/eth/v2/debug/beacon/states/$1"
