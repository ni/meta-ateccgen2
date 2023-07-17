LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

PACKAGE_ARCH = "${MACHINE_ARCH}"

inherit systemd

SRC_URI += " \
    file://post-update-sanity-check \
    file://post-update-sanity-check.service \
"

FILES:${PN} = " \
    ${bindir} \
    ${systemd_system_unitdir} \
"

SYSTEMD_SERVICE:${PN} = " \
    post-update-sanity-check.service \
"

do_install () {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/post-update-sanity-check ${D}${bindir}
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/post-update-sanity-check.service ${D}${systemd_system_unitdir}
}
