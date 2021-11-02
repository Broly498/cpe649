#!/bin/sh

set -x
set -e
echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind
