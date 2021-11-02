#!/bin/sh

set -x
set -e

# This script accepts two command-line arguments:
# argv1 - FTP Server IP Address
# argv2 - FTP Server Port
# argv3 - Encryption Data Client IP Address

FTP_SERVER_IP_ADDRESS=$1
FTP_SERVER_PORT=$2
ENCRYPTION_DATA_CLIENT_IP_ADDRESS=$3

if [ -z "$FTP_SERVER_IP_ADDRESS" ]
  then
    echo "FTP Server IP address was not supplied, defaulting to localhost..."
   FTP_SERVER_IP_ADDRESS=localhost
fi

if [ -z "$FTP_SERVER_PORT" ]
  then
    echo "FTP Server port was not supplied, defaulting to 21..."
    FTP_SERVER_PORT=21
fi

if [ -z "$ENCRYPTION_DATA_CLIENT_IP_ADDRESS" ]
  then
    echo "Encryption Data Client IP address was not supplied, defaulting to 0.0.0.0..."
    ENCRYPTION_DATA_CLIENT_IP_ADDRESS=0.0.0.0
fi

IMAGE_GENERATION_DIRECTORY=examples
POWER_MEASUREMENT_DIRECTORY=PiHat/build
PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY=powerMeasurementResults

mkdir -p $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY

current_time=$(date "+%Y_%m_%d-%H_%M_%S")

PROFILER_IDLE_TIME_s=300

sudo nice -n -20 sudo taskset 0x8 ./$POWER_MEASUREMENT_DIRECTORY/profiler -p -t 10 > $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY/${current_time}_ImageEncryptorPiHatResuls.csv & sleep $PROFILER_IDLE_TIME_s
python3 $IMAGE_GENERATION_DIRECTORY/networked-encrypt-image-data.py $ENCRYPTION_DATA_CLIENT_IP_ADDRESS $FTP_SERVER_IP_ADDRESS $FTP_SERVER_PORT &
