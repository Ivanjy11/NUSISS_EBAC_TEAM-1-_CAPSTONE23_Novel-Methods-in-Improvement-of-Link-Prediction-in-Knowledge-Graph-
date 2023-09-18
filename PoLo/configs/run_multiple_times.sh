#!/bin/bash

# This is the script that will be run multiple times
SCRIPT_TO_RUN="./run.sh"
CONFIG_FILE="configs/my_config.sh"

# Number of times to run the script
NUM_RUNS=5

# Loop to run the script multiple times
for ((i=1; i<=$NUM_RUNS; i++)); do
    echo "Running the script: $i"
    $SCRIPT_TO_RUN $CONFIG_FILE
    echo "Completed run $i"
    echo
done
