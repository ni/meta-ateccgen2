LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "\
    file://mfgconfig.json \
"

FILES_${PN} += " /data/rcu-service/config/* "

do_install () {
    install -d ${D}/data/rcu-service/config
    install -m 0644 ${WORKDIR}/mfgconfig.json ${D}/data/rcu-service/config
}

