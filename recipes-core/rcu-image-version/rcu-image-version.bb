LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "\
    file://rcu-image-version \
"

do_install () {
    install -d ${D}${sysconfdir}
    install -m 0644 ${WORKDIR}/rcu-image-version ${D}${sysconfdir}
}
