#!/usr/bin/env fish

echo "Fetching head state..."
state.sh head > head_state.json
echo "Extracting votes..."
./analyse.py
