#!/usr/bin/env sh
#
# Called from udev. Compatible to apalis-imx8x.
#
# Create/remove symlinks to/from the files with raw ain data.

# Map the ADC lines:
# apalis-adc{0..3} -> ADMA.ADC.IN{0,1,4,5}

if [ "$ACTION" = "add" ]; then
    ln -s "/sys$DEVPATH/in_voltage0_raw" /dev/apalis-adc0
    ln -s "/sys$DEVPATH/in_voltage1_raw" /dev/apalis-adc1
    ln -s "/sys$DEVPATH/in_voltage4_raw" /dev/apalis-adc2
    ln -s "/sys$DEVPATH/in_voltage5_raw" /dev/apalis-adc3
elif [ "$ACTION" = "remove" ]; then
    rm -f /dev/apalis-adc0
    rm -f /dev/apalis-adc1
    rm -f /dev/apalis-adc2
    rm -f /dev/apalis-adc3
fi

