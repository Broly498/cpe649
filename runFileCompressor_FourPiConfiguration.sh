#!/bin/sh

set -x
set -e

# This script accepts one command-line arguments:
# argv1 - Compression Data Client IP Address

COMPRESSION_DATA_CLIENT_IP_ADDRESS=$1

if [ -z "$COMPRESSION_DATA_CLIENT_IP_ADDRESS" ]
  then
    echo "Compression Data Client IP address was not supplied, defaulting to localhost..."
    COMPRESSION_DATA_CLIENT_IP_ADDRESS=localhost
fi

IMAGE_GENERATION_DIRECTORY=examples
POWER_MEASUREMENT_DIRECTORY=PiHat/build
PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY=powerMeasurementResults

mkdir -p $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY

current_time=$(date "+%Y_%m_%d-%H_%M_%S")

PROFILER_IDLE_TIME_s=300

sudo nice -n -20 sudo taskset 0x8 ./$POWER_MEASUREMENT_DIRECTORY/profiler -p -t 10 > $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY/${current_time}_CompressionDataClientPiHatResuls.csv & sleep $PROFILER_IDLE_TIME_s
python3 $IMAGE_GENERATION_DIRECTORY/networked-compress-image-data.py $COMPRESSION_DATA_CLIENT_IP_ADDRESS &
