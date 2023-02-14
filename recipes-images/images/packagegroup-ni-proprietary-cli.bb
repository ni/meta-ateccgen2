SUMMARY = "SmartRacks packagegroups which provide proprietary cmdline releated packages"

PACKAGE_ARCH = "${MACHINE_ARCH}"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES += " \
    packagegroup-base-ni-proprietary-cli \
"

RDEPENDS_packagegroup-ni-proprietary-cli = "\
    packagegroup-base-ni-proprietary-cli \
"

SUMMARY_packagegroup-base-ni-proprietary-cli = "Proprietary packages preinstalled into SmartRacks RCU image"
RRECOMMENDS_packagegroup-base-ni-proprietary-cli = "\
    rcu-service \
"
