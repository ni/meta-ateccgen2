FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

# This .cfg file is applied on top of the Apalis iMX8X defconfig
# as specified in the linux-toradex recipe in meta-toradex-nxp
# https://git.toradex.com/cgit/meta-toradex-nxp.git/tree/recipes-kernel/linux/linux-toradex_5.4-2.1.x.bb?h=dunfell-5.x.y

SRC_URI += " \
    file://smartracks.cfg \
    file://add-support-for-diodes-pi4ioe5v96248.patch \
    file://0001-hwmon-add-support-for-SMSC-EMC2303.patch \
    "

# Inject SmartRacks custom board device tree to kernel source device tree location
