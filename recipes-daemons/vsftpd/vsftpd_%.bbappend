FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

do_install_append(){
    install -m 644 ${WORKDIR}/vsftpd.conf ${D}${sysconfdir}
}
