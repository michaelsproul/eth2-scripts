#!/usr/bin/env python3

# Usage: ./import_attester_slashings.py op_pool.json slashed_validators.txt
# + op_pool.json is a JSON dump from Lighthouse's /advanced/op_pool endpoint
# + slashed_validators.txt is a text file of already slashed validators,
#   as produced by `get_slashed.sh`. Can be empty if you don't mind waiting.
# FIXME: needs updating for standard API

import sys
import json
import time
import http.client

LH_HOST = "localhost:5052"
IMPORT_DELAY = 2
SHOULD_IMPORT = True
KEEP_GOING = True

def get_useful_slashings(op_pool_filename, slashed_validators_filename):
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
            new_slashed_validators.update(new_slashed_indices)
            useful_slashings.append(slashing)

    print("Found {} useful slashings and {} validators to slash".format(len(useful_slashings), len(new_slashed_validators)))
    return useful_slashings

def import_to_beacon_node(useful_slashings):
    total_slashings = len(useful_slashings)
    for (i, slashing) in enumerate(useful_slashings):
        print("Importing useful attestation {} of {}".format(i + 1, total_slashings))
        conn = http.client.HTTPConnection(LH_HOST)
        conn.request("POST", "/beacon/attester_slashing", body=json.dumps(slashing))
        res = conn.getresponse()
        if res.status != 200:
            body = res.read()
            if res.status == 400 and body == b"Attester slashing only covers already slashed indices":
                print("Already known")
            else:
                print("Failed with status {}".format(res.status))
                print(body)

            if not KEEP_GOING:
                print("Exiting!")
                exit(1)
        time.sleep(IMPORT_DELAY)

def main():
    useful_slashings = get_useful_slashings(sys.argv[1], sys.argv[2])
    if SHOULD_IMPORT:
        import_to_beacon_node(useful_slashings)

if __name__ == "__main__":
    main()
