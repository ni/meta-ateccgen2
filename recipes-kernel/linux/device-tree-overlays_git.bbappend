TEZI_EXTERNAL_KERNEL_DEVICETREE_BOOT:apalis-imx8 = " apalis-imx8_hdmi_overlay.dtbo "

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://apalis-imx8_multirack-1rack_overlay.dts \
    file://apalis-imx8_multirack-2rack_overlay.dts \
    file://apalis-imx8_multirack-3rack_overlay.dts \
"

do_collect_overlays:prepend() {
    # Copy custom overlays into Toradex workdir defined in toradex-devicetree.bbclass
    cp ${WORKDIR}/apalis-imx8_multirack-1rack_overlay.dts ${S}
    cp ${WORKDIR}/apalis-imx8_multirack-2rack_overlay.dts ${S}
    cp ${WORKDIR}/apalis-imx8_multirack-3rack_overlay.dts ${S}
}

