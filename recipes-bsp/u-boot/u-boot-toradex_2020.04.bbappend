FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://alter-default-apalis-device-tree.patch \
    file://enable-u-boot-eth1.patch \
"
