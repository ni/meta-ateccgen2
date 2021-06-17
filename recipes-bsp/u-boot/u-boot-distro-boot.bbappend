FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " file://set-gpio-direction-uboot.patch;patchdir=${WORKDIR} "
