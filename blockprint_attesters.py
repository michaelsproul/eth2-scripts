#!/usr/bin/env python3

import os
import csv
import sys
import json
import requests

USERNAME = os.environ["BLOCKPRINT_USERNAME"]
PASSWORD = os.environ["BLOCKPRINT_PASSWORD"]
URL = "https://api.blockprint.sigp.io/validator/blocks"
CLIENTS = ["Prysm", "Lighthouse", "Teku", "Nimbus", "Lodestar", "Unknown"]

def get_validator_blocks(indices):
    res = requests.post(URL, auth=(USERNAME, PASSWORD), json=indices)
    res.raise_for_status()
    return res.json()

def main():
    indexed_attestation_file = sys.argv[1]
    with open(indexed_attestation_file, "r") as f:
        indexed_attestations = json.load(f)

    # Map from slot and beacon block root to validators voting for that root.
    attesters_by_slot_and_root = {}

    # Map from validator index to client guess (assumes no equivocation).
    attester_clients = {}

    for attestation in indexed_attestations:
        block_root = attestation["data"]["beacon_block_root"]
        slot = int(attestation["data"]["slot"])

        attesting_indices = list(map(int, attestation["attesting_indices"]))
        new_attesting_indices = [idx for idx in attesting_indices if idx not in attester_clients]

        for idx in attesting_indices:
            if (slot, block_root) not in attesters_by_slot_and_root:
                attesters_by_slot_and_root[(slot, block_root)] = set()
            attesters_by_slot_and_root[(slot, block_root)].add(idx)

        if len(new_attesting_indices) == 0:
            print("all validators already known, skipping")
            continue

        print(f"loading blockprint data for {len(new_attesting_indices)} new attesters")
        all_blocks = get_validator_blocks(new_attesting_indices)

        for (idx_str, blocks) in all_blocks.items():
            idx = int(idx_str)

            best_guess = "Unknown" if blocks == [] else blocks[-1]["best_guess_single"]

            attester_clients[idx] = best_guess


    # Count clients per vote.
    rows = []
    for ((slot, block_root), attesters) in attesters_by_slot_and_root.items():
        per_client_counts = {client: 0 for client in CLIENTS}

        for attester in attesters:
            client = attester_clients[attester]
            per_client_counts[client] += 1

        c = per_client_counts
        row = [
            slot,
            block_root,
            c["Prysm"], c["Lighthouse"], c["Teku"], c["Nimbus"], c["Lodestar"], c["Unknown"]
        ]
        rows.append(row)

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["slot", "block_root", "Prysm", "Lighthouse", "Teku", "Nimbus", "Lodestar", "Unknown"])

        for row in rows:
            writer.writerow(row)

if __name__ == "__main__":
    main()
