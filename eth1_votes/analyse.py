#!/usr/bin/env python3

import json
from collections import namedtuple

Eth1DataVote = namedtuple("Eth1DataVote", ["deposit_root", "deposit_count", "block_hash"])

def eth1_data_vote(v):
    return Eth1DataVote(v["deposit_root"], int(v["deposit_count"]), v["block_hash"])

def count_vote(target_vote, votes):
    return len([1 for vote in votes if vote == target_vote])

state = json.load(open("head_state.json"))
votes = [eth1_data_vote(vote) for vote in state["data"]["eth1_data_votes"]]
uniq_votes = set(votes)
vote_counts = {vote: count_vote(vote, votes) for vote in uniq_votes}

current_block_hash = state["data"]["eth1_data"]["block_hash"]

for (vote, count) in sorted(vote_counts.items(), key=lambda v: (-v[1], v[0].block_hash, -v[0].deposit_count)):
    description = " (incumbent)" if vote.block_hash == current_block_hash else ""
    print("{}[{}]: {}{}".format(vote.block_hash, vote.deposit_count, count, description))

slot = int(state["data"]["slot"])
slots_remaining = 2048 - (slot % 2048) - 1
print("total votes in period: {}, slots remaining: {}".format(len(votes), slots_remaining))
print("participation: {}%".format(round(100 * len(votes) / (slot % 2048), 2)))
