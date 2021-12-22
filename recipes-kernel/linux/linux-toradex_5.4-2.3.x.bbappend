FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

# This .cfg file is applied on top of the Apalis iMX8X defconfig
# as specified in the linux-toradex recipe in meta-toradex-nxp
# https://git.toradex.com/cgit/meta-toradex-nxp.git/tree/recipes-kernel/linux/linux-toradex_5.4-2.1.x.bb?h=dunfell-5.x.y

SRC_URI += " \
    file://smartracks.cfg \
    file://imx8qxp-apalis-smartracks.dtsi \
    file://imx8qxp-apalis-smartracks.dts \
    file://add-support-for-diodes-pi4ioe5v96248.patch \
    file://hwmon-add-support-for-SMSC-EMC2305-03-02-01-fan-controller.patch \
    "

# Inject SmartRacks custom board device tree to kernel source device tree location
do_configure_prepend() {
    cp ${WORKDIR}/imx8qxp-apalis-smartracks.dtsi ${WORKDIR}/git/arch/arm64/boot/dts/freescale
    cp ${WORKDIR}/imx8qxp-apalis-smartracks.dts ${WORKDIR}/git/arch/arm64/boot/dts/freescale
}
