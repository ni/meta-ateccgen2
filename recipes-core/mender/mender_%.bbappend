FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append = " file://ateccgen2_rsa_public.key \
                   file://mender.conf \
                   file://rcu-mender-image-firstboot \
                   file://0001-Save-pending-commit-state-as-version-1.patch \
"

do_install:append() {
    install -d ${D}${sysconfdir}/mender
    install -m 0644 ${WORKDIR}/ateccgen2_rsa_public.key ${D}${sysconfdir}/mender
    install -m 0644 ${WORKDIR}/rcu-mender-image-firstboot ${D}${sysconfdir}/mender
}

# On scarthgap the recipe is "mender" and its files are split across the mender-auth, mender-update and
# mender-config packages, so files installed above must be assigned to a package explicitly.
FILES:mender-update += " \
    ${sysconfdir}/mender/ateccgen2_rsa_public.key \
    ${sysconfdir}/mender/rcu-mender-image-firstboot \
"

# Disable Mender to run as a system service automatically at boot as refer to 
# https://docs.mender.io/system-updates-yocto-project/customize-mender#disabling-mender-as-a-system-service
# Comment out line below to enable mender running as a systemd service as it has been enabled in meta-mender/meta-mender-core/recipes-mender/mender-client.inc
SYSTEMD_AUTO_ENABLE = "disable"
