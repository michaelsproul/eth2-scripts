#!/bin/bash

curl -s "http://localhost:5052/eth/v1/beacon/states/head/validators/$1" | jq .data
