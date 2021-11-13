#!/bin/sh

set -x
set -e

# This script accepts two command-line arguments:
# argv1 - Sampling Rate (ms)
# argv2 - Experiment Name

SAMPLING_RATE_ms=$1
EXPERIMENT_NAME=$2

if [ -z "$SAMPLING_RATE_ms" ]
  then
    echo "Sampling rate was not provided, defaulting to 10 ms..."
    SAMPLING_RATE_ms=10
fi

if [ -z "$EXPERIMENT_NAME" ]
  then
    EXPERIMENT_NAME=idleRun
fi

POWER_MEASUREMENT_DIRECTORY=PiHat/build
PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY=powerMeasurementResults

mkdir -p $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY

current_time=$(date "+%Y_%m_%d-%H_%M_%S")

sudo nice -n -20 sudo taskset 0x8 ./$POWER_MEASUREMENT_DIRECTORY/profiler -p -t $SAMPLING_RATE_ms > $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY/${current_time}_${EXPERIMENT_NAME}PiHatResuls.csv &
