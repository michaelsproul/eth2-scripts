#!/usr/bin/env fish

# Usage: ./participation_rate.fish 3150
# Requires: fish, curl, jq, Lighthouse BN API on port 5052
# Set the target epoch to at least 2 before the current epoch
set target_epoch (math "$argv[1] + 1")

set global_votes (curl --fail --show-error -s "http://localhost:5052/lighthouse/validator_inclusion/$target_epoch/global"; or exit)
set global_votes (echo $global_votes | jq .data)
set prev_active_gwei (echo $global_votes | jq .previous_epoch_active_gwei)
set prev_target_gwei (echo $global_votes | jq .previous_epoch_target_attesting_gwei)
set curr_active_gwei (echo $global_votes | jq .current_epoch_active_gwei)
set participation_rate_current (math "$prev_target_gwei / $prev_active_gwei")
set participation_rate_prev (math "$prev_target_gwei / $curr_active_gwei")
set prev_epoch (math "$target_epoch - 1")
echo "Epoch: $prev_epoch"
echo "Active GWei (as current): $prev_active_gwei"
echo "Active GWei (as previous): $curr_active_gwei"
echo "Matching target GWei: $prev_target_gwei"
echo "Participation rate (as current epoch): $participation_rate_current"
echo "Participation rate (as previous epoch): $participation_rate_prev"
