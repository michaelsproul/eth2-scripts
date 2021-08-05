#!/usr/bin/env bash

source $(eth2_scripts_dir.sh)/setup.sh

curl "$BEACON_NODE/eth/v1/node/peers?state=connected"
