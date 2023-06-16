require ateccgen2-base-image.inc

SUMMARY = "NI ATE Core Configurations Gen 2 RCU Image"
DESCRIPTION = "NI ATE Core Configurations Gen 2 RCU image with proprietary RCU firmware"

IMAGE_INSTALL += " \
    packagegroup-base-ni-cli \
    packagegroup-base-ni-proprietary-cli \
"
