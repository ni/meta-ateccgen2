FILESEXTRAPATHS_prepend := "${THISDIR}/files/:"

# The 99-toradex.rules from apalis-imx8 defines a set of apalis specific SYMLINKs which are not applicable to smartracks.
# It is pulled in by bitbake because we use the default apalis-imx8 instead of creating a new custom smartracks MACHINE.
# Hence, this bbappend is added to remove 99-toradex.rules entirely.

do_install_append() {
    rm -f ${D}${sysconfdir}/udev/rules.d/99-toradex.rules
}
