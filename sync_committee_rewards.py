import requests
import os
import sys

BEACON_NODE = os.environ.get("BEACON_NODE") or "http://localhost:5052"
SLOTS_PER_EPOCH = 32

def main():
    epoch = int(sys.argv[1])

    slots = [epoch * SLOTS_PER_EPOCH + i for i in range(0, SLOTS_PER_EPOCH)]

    validator_rewards = {}

    for slot in slots:
        res = requests.post(f"{BEACON_NODE}/eth/v1/beacon/rewards/sync_committee/{slot}", json=[])

        # omit skipped slots, no rewards or penalties paid if there's no block
        if res.status_code == 404:
            continue
        res.raise_for_status()

        slot_rewards = res.json()["data"]

        for item in slot_rewards:
            validator_index = int(item["validator_index"])
            reward = int(item["reward"])

            if validator_index not in validator_rewards:
                validator_rewards[validator_index] = reward
            else:
                validator_rewards[validator_index] += reward

    print(f"sync committee rewards for epoch {epoch}")
    for validator_index in sorted(validator_rewards.keys()):
        print("{}: {} gwei".format(validator_index, validator_rewards[validator_index]))

if __name__ == "__main__":
    main()
