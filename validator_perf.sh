#!/bin/bash
# Usage: ./validator_perf.sh EPOCH VALIDATOR_INDEX

curl -s "http://localhost:5052/lighthouse/validator_inclusion/$1/$2" | jq .data
