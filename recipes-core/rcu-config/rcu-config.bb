LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "\
    file://mfgconfig.json \
    file://userconfig.json \
"

do_install () {
    install -d ${D}${sysconfdir}
    install -m 0644 ${WORKDIR}/mfgconfig.json ${D}${sysconfdir}
    install -m 0644 ${WORKDIR}/userconfig.json ${D}${sysconfdir}
}
