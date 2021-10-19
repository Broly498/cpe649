#!/bin/sh

set -x
set -e

IMAGE_GENERATION_DIRECTORY=examples

# Note: Default image boundary: -90.9217, 14.4191, -90.8187, 14.5520
# Has been split into quarters with half-way points: -90.8702, 14.4855

taskset 0x1 python3 $IMAGE_GENERATION_DIRECTORY/sentinel2-cloud-detector-example.py -90.9217 14.4191 -90.8702 14.4855 &
sleep 2
taskset 0x2 python3 $IMAGE_GENERATION_DIRECTORY/sentinel2-cloud-detector-example.py -90.9217 14.4855 -90.8702 14.5520 &
sleep 2
taskset 0x4 python3 $IMAGE_GENERATION_DIRECTORY/sentinel2-cloud-detector-example.py -90.8702 14.4191 -90.8187 14.4855 &
sleep 2
taskset 0x8 python3 $IMAGE_GENERATION_DIRECTORY/sentinel2-cloud-detector-example.py -90.8702 14.4855 -90.8187 14.5520 &
