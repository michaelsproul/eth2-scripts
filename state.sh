#!/bin/bash

curl -s "http://localhost:5052/eth/v1/debug/beacon/states/$1"
