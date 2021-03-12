FILESEXTRAPATHS_prepend := "${THISDIR}/files/:"

SRC_URI_append = " file://vsftpd-sd.rules \
                   file://vsftpd-sd.sh \
"

do_install_append() {
    install -d ${D}${sysconfdir}/udev/rules.d
    install -m 0644 ${WORKDIR}/vsftpd-sd.rules ${D}${sysconfdir}/udev/rules.d/vsftpd-sd.rules

    install -d ${D}${sysconfdir}/udev/scripts/
    install -m 0755 ${WORKDIR}/vsftpd-sd.sh ${D}${sysconfdir}/udev/scripts/vsftpd-sd.sh
}
