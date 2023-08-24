FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append = " file://ateccgen2-rsa-public.key \
                   file://mender.conf \
"

# Disable Mender to run as a system service automatically at boot as refer to 
# https://docs.mender.io/system-updates-yocto-project/customize-mender#disabling-mender-as-a-system-service
# Comment out line below to enable mender running as a systemd service as it has been enabled in meta-mender/meta-mender-core/recipes-mender/mender-client.inc
SYSTEMD_AUTO_ENABLE = "disable"
