#!/usr/bin/env python3

# Backfill blocks from another beacon node using the HTTP API - slow, for debugging only

import json
from http.client import HTTPConnection

LOCAL_BEACON = "localhost:5052"
REMOTE_BEACON = "localhost:8000"
BATCH_SIZE = 50

def main():
    local = HTTPConnection(LOCAL_BEACON)
    local.request("GET", "/lighthouse/database/info")
    db_info = json.loads(local.getresponse().read().decode())

    oldest_block_slot = int(db_info["anchor"]["oldest_block_slot"])

    print("oldest block slot", oldest_block_slot)

    remote = HTTPConnection(REMOTE_BEACON)

    while oldest_block_slot > 0:
        blocks = []
        batch_start = max(0, oldest_block_slot - BATCH_SIZE)
        batch_end  = oldest_block_slot
        for slot in range(batch_start, batch_end):
            remote.request("GET", "/eth/v1/beacon/blocks/{}".format(slot))
            res = remote.getresponse()
            json_res = json.loads(res.read().decode())
            if res.status == 404:
                # no block at this slot
                continue
            elif res.status != 200:
                raise Exception("error response from remote: {}".format(json_res))
            blocks.append(json_res["data"])

        body = json.dumps(blocks)
        local.request("POST", "/lighthouse/database/historical_blocks", body=body)
        res = local.getresponse()
        res_json = json.loads(res.read().decode())
        assert res.status == 200
        oldest_block_slot = int(res_json["oldest_block_slot"])

        remaining = max(oldest_block_slot - 1, 0)
        print("uploaded {} blocks, {} remaining".format(batch_end - batch_start, remaining))

if __name__ == "__main__":
    main()
