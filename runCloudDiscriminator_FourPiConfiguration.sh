#!/bin/sh

set -x
set -e

# This script accepts two command-line arguments:
# argv1 - Image Data Client IP Address

IMAGE_DATA_CLIENT_IP_ADDRESS=$1

if [ -z "$IMAGE_DATA_CLIENT_IP_ADDRESS" ]
  then
    echo "Image Data Client IP address was not supplied, defaulting to localhost..."
    IMAGE_DATA_CLIENT_IP_ADDRESS=localhost
fi

IMAGE_GENERATION_DIRECTORY=examples
POWER_MEASUREMENT_DIRECTORY=PiHat/build
PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY=powerMeasurementResults

mkdir -p $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY

current_time=$(date "+%Y_%m_%d-%H_%M_%S")

PROFILER_IDLE_TIME_s=300

sudo taskset 0x8 ./$POWER_MEASUREMENT_DIRECTORY/profiler -p -t 10 > $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY/${current_time}_CloudDiscriminatorPiHatResuls.csv & sleep $PROFILER_IDLE_TIME_s
taskset 0x4 python3 $IMAGE_GENERATION_DIRECTORY/networked-cloud-discrimination.py $IMAGE_DATA_CLIENT_IP_ADDRESS &
