#!/usr/bin/env python3

import sys
import json

def main():
    op_pool_filename = sys.argv[1]
    slashed_validators_filename = sys.argv[2]
    op_pool = None
    already_slashed_validators = None
    with open(op_pool_filename, "r") as f:
        op_pool = json.load(f)
    with open(slashed_validators_filename) as f:
        already_slashed_validators = set(int(x) for x in f.readlines())

    useful_slashings = []
    new_slashed_validators = set()

    for [slashing, _] in op_pool["attester_slashings"]:
        att1_indices = set(slashing["attestation_1"]["attesting_indices"])
        att2_indices = set(slashing["attestation_2"]["attesting_indices"])
        slashed_indices = att1_indices.intersection(att2_indices)
        new_slashed_indices = slashed_indices - already_slashed_validators - new_slashed_validators

        if len(new_slashed_indices) > 0:
            print("slashing of {} indices, {} new".format(len(slashed_indices), len(new_slashed_indices)))
            new_slashed_validators.update(new_slashed_indices)

    print("total validators remaining to slash: {}".format(len(new_slashed_validators)))

if __name__ == "__main__":
    main()
