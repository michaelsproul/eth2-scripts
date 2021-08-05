# Set Bash options
set -o errexit -o pipefail -o nounset
shopt -s expand_aliases

# Set up the Eth2 beacon node URL, either from the environment variable BEACON_NODE
# or the default http://localhost:5052
#
# This script should be `source`d rather than executed
export BEACON_NODE="${BEACON_NODE:-http://localhost:5052}"

# Set up curl to fail on errors from the remote.
alias curl="curl --fail --no-progress-meter"
