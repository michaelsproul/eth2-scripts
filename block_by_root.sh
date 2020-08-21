#!/bin/bash

curl -s "http://localhost:5052/beacon/block?root=$1" | jq
