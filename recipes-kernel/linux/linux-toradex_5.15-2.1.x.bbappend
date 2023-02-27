FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# This .cfg file is applied on top of the Toradex defconfig
# as specified in the linux-toradex recipe in meta-toradex-nxp
# https://git.toradex.com/cgit/meta-toradex-nxp.git/tree/recipes-kernel/linux/linux-toradex_5.15-2.1.x.bb?h=kirkstone-6.x.y

SRC_URI += " \
    file://smartracks.cfg \
    file://imx8-apalis-smartracks.dtsi \
    file://imx8-apalis-smartracks.dts \
    file://add-support-for-diodes-pi4ioe5v96248.patch \
    file://0001-hwmon-add-support-for-SMSC-EMC2303.patch \
    "

# Inject SmartRacks custom board device tree to kernel source device tree location
do_configure:prepend() {
    cp ${WORKDIR}/imx8-apalis-smartracks.dtsi ${WORKDIR}/git/arch/arm64/boot/dts/freescale
    cp ${WORKDIR}/imx8-apalis-smartracks.dts ${WORKDIR}/git/arch/arm64/boot/dts/freescale
}
