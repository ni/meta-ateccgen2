SUMMARY = "SmartRacks packagegroups which provide proprietary cmdline releated packages"

PACKAGE_ARCH = "${MACHINE_ARCH}"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES += " \
    packagegroup-base-ni-proprietary-cli \
    packagegroup-devel-ni-proprietary-cli \
"

RDEPENDS_packagegroup-ni-proprietary-cli = "\
    packagegroup-base-ni-proprietary-cli \
    packagegroup-devel-ni-proprietary-cli \
"

SUMMARY_packagegroup-base-ni-proprietary-cli = "Proprietary packages preinstalled into SmartRacks RCU image"
RRECOMMENDS_packagegroup-base-ni-proprietary-cli = "\
    rcu-service \
"

SUMMARY_packagegroup-devel-ni-proprietary-cli = "Proprietary tools useful during SmartRacks RCU development"
RRECOMMENDS_packagegroup-devel-ni-proprietary-cli = "\
    rcu-service-python-test-client \
"
