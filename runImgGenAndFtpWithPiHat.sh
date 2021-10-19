#!/bin/sh

set -x
set -e

IMAGE_GENERATION_DIRECTORY=examples
POWER_MEASUREMENT_DIRECTORY=PiHat/build
PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY=powerMeasurementResults

mkdir -p $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY

taskset 0x1 python3 $IMAGE_GENERATION_DIRECTORY/networked-encrypt-image-data.py & sleep 10
taskset 0x2 python3 $IMAGE_GENERATION_DIRECTORY/networked-compress-image-data.py & sleep 10
taskset 0x4 python3 $IMAGE_GENERATION_DIRECTORY/networked-cloud-discrimination.py & sleep 10
sudo taskset 0x8 ./$POWER_MEASUREMENT_DIRECTORY/profiler -p -t 10 > $PI_HAT_POWER_MEASUREMENTS_OUTPUT_DIRECTORY/piHatResults.csv
