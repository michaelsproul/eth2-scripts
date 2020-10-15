#!/bin/bash

curl -s "http://localhost:5052/eth/v1/debug/beacon/heads" | jq .data
