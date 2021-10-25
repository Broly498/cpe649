#!/bin/sh

set -x
set -e

# This script accepts two command-line arguments:
# argv1 - FTP Server IP Address
# argv2 - FTP Server Port
# argv3 - Compression Data Client IP Address
# argv4 - Image Data Client IP Address

COMPRESSION_DATA_CLIENT_IP_ADDRESS=$3
IMAGE_DATA_CLIENT_IP_ADDRESS=$4

if [ -z "$COMPRESSION_DATA_CLIENT_IP_ADDRESS" ]
  then
    echo "Compression Data Client IP address was not supplied, defaulting to localhost..."
    COMPRESSION_DATA_CLIENT_IP_ADDRESS=localhost
fi

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

taskset 0x1 python3 $IMAGE_GENERATION_DIRECTORY/networked-encrypt-image-data.py $1 $2  & sleep 10
taskset 0x2 python3 $IMAGE_GENERATION_DIRECTORY/networked-compress-image-data.py $3 & sleep 10
taskset 0x4 python3 $IMAGE_GENERATION_DIRECTORY/networked-cloud-discrimination.py $4 & sleep 10
sudo taskset 0x8 ./$POWER_MEASUREMENT_DIRECTORY/profiler -p -t 10 > $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY/${current_time}_piHatResuls.csv
