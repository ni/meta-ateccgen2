FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# vsftpd service availability is handled using udev rules
SYSTEMD_AUTO_ENABLE_${PN} = "disable"

do_install:append(){

    install -d ${D}${localstatedir}/lib/ftp
    chown -R nobody:nogroup ${D}${localstatedir}/lib/ftp
    chmod -R 775 ${D}${localstatedir}/lib/ftp

    install -d ${D}${localstatedir}/lib/ftp/upload
    chown -R ftp:ftp ${D}${localstatedir}/lib/ftp/upload
    chmod -R 777 ${D}${localstatedir}/lib/ftp/upload

    install -m 644 ${WORKDIR}/vsftpd.conf ${D}${sysconfdir}
}
