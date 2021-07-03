#!/usr/bin/env python3

import json

def count_vote(block_hash, votes):
    return len([1 for vote in votes if vote["block_hash"] == block_hash])

votes = json.load(open("eth1_data_votes.json"))
block_hashes = set(v["block_hash"] for v in votes)
uniq_votes = {block_hash: count_vote(block_hash, votes) for block_hash in block_hashes}

for (block_hash, count) in uniq_votes.items():
    print("{}: {}".format(block_hash, count))

print("total votes in period: {}, remaining: {}".format(len(votes), 2048 - len(votes)))
