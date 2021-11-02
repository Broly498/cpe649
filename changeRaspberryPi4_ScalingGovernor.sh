#!/bin/sh

# This script accepts two command-line arguments:
# argv1 - Scaling Governor Option (powersave=0, performance=1, ondemand=2)

if [ -z "$1" ]
  then
    echo "Scaling Governor option was not supplied, defaulting to powersave..."
    SCALING_GOVERNOR=powersave
elif [ "$1" -eq 0 ]
  then
    echo "Powersave Scaling Governor was selected..."
    SCALING_GOVERNOR=powersave
elif [ "$1" -eq 1 ]
  then
    echo "Performance Scaling Governor was selected..."
    SCALING_GOVERNOR=performance
elif [ "$1" -eq 2 ]
  then
    echo "Ondemand Scaling Governor was selected..."
    SCALING_GOVERNOR=ondemand
else
    echo "Invalid command-line argument was supplied, argv1 must equal one of the following integer values: (powersave=0, performance=1, ondemand=2)..."
    exit 1
fi

sudo echo "$SCALING_GOVERNOR" | sudo tee -a /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
