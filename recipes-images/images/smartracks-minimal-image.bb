require smartracks-base-image.inc

SUMMARY = "Smart Racks RCU Image"
DESCRIPTION = "Smart Racks RCU image"

IMAGE_INSTALL += " \
    packagegroup-base-ni-cli \
"
