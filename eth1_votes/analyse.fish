#!/usr/bin/env fish

echo "Fetching head state..."
state.sh head > head_state.json
echo "Extracting votes..."
jq .data.eth1_data_votes < head_state.json > eth1_data_votes.json
./analyse.py
