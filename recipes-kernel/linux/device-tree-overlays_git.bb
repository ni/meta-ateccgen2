SUMMARY = "SmartRack device tree overlays"
DESCRIPTION = "SmartRack device tree overlays from within the layer."

SRC_URI = "file://smartrack_overlay.dts file://template_overlay.dts"

inherit devicetree

S = "${WORKDIR}"

COMPATIBLE_MACHINE = "apalis-imx8x-smartrack"

# we have dtbo's in arm and arm64 architecture, set the include paths
# to include both architectures.
KERNEL_INCLUDE = " \
    ${STAGING_KERNEL_DIR}/arch/arm/boot/dts \
    ${STAGING_KERNEL_DIR}/arch/arm/boot/dts*/* \
    ${STAGING_KERNEL_DIR}/arch/arm64/boot/dts \
    ${STAGING_KERNEL_DIR}/arch/arm64/boot/dts/* \
    ${STAGING_KERNEL_DIR}/scripts/dtc/include-prefixes \
"
