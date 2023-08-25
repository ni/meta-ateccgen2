FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append = " file://ateccgen2_rsa_public.key \
                   file://mender.conf \
"

do_install:append() {
    install -d ${D}${sysconfdir}/mender
    install -m 0644 ${WORKDIR}/ateccgen2_rsa_public.key ${D}${sysconfdir}/mender
}

# Disable Mender to run as a system service automatically at boot as refer to 
# https://docs.mender.io/system-updates-yocto-project/customize-mender#disabling-mender-as-a-system-service
# Comment out line below to enable mender running as a systemd service as it has been enabled in meta-mender/meta-mender-core/recipes-mender/mender-client.inc
SYSTEMD_AUTO_ENABLE = "disable"
