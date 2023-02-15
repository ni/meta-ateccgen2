require smartracks-base-image.inc

SUMMARY = "Smart Racks RCU Image"
DESCRIPTION = "Smart Racks RCU image with proprietary RCU firmware"

IMAGE_INSTALL += " \
    packagegroup-base-ni-cli \
    packagegroup-base-ni-proprietary-cli \
"
