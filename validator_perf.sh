#!/usr/bin/env bash
# Usage: ./validator_perf.sh EPOCH VALIDATOR_INDEX

source $(eth2_scripts_dir.sh)/setup.sh

curl "$BEACON_NODE/lighthouse/validator_inclusion/$1/$2" | jq .data
