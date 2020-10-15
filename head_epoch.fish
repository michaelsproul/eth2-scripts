#!/usr/bin/env fish

set head_slot (curl -s "http://localhost:5052/eth/v1/node/syncing" | jq .data.head_slot)
echo (math "floor($head_slot / 32)")
