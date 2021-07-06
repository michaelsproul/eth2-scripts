#!/usr/bin/env python3

import json

def count_vote(block_hash, votes):
    return len([1 for vote in votes if vote["block_hash"] == block_hash])

state = json.load(open("head_state.json"))
votes = state["data"]["eth1_data_votes"]
slot = int(state["data"]["slot"])
current_block_hash = state["data"]["eth1_data"]["block_hash"]
block_hashes = set(v["block_hash"] for v in votes)
uniq_votes = {block_hash: count_vote(block_hash, votes) for block_hash in block_hashes}

for (block_hash, count) in sorted(uniq_votes.items(), key=lambda v: -v[1]):
    if block_hash == current_block_hash:
        print("{}: {} (incumbent)".format(block_hash, count))
    else:
        print("{}: {}".format(block_hash, count))

slots_remaining = 2048 - (slot % 2048) - 1
print("total votes in period: {}, slots remaining: {}".format(len(votes), slots_remaining))
print("participation: {}%".format(round(100 * len(votes) / (slot % 2048), 2)))
