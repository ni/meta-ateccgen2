FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

do_install_append(){

    install -d ${D}${localstatedir}/lib/ftp
    chown -R nobody:nogroup ${D}${localstatedir}/lib/ftp
    chmod -R 775 ${D}${localstatedir}/lib/ftp

    install -d ${D}${localstatedir}/lib/ftp/upload
    chown -R ftp:ftp ${D}${localstatedir}/lib/ftp/upload
    chmod -R 777 ${D}${localstatedir}/lib/ftp/upload

    install -m 644 ${WORKDIR}/vsftpd.conf ${D}${sysconfdir}
}
