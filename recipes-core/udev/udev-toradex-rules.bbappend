FILESEXTRAPATHS_prepend := "${THISDIR}/files/:"

do_install_append() {
    rm -f ${D}${sysconfdir}/udev/rules.d/99-toradex.rules
}
