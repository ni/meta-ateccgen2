SUMMARY = "SmartRacks packagegroups which provide cmdline releated packages"

PACKAGE_ARCH = "${MACHINE_ARCH}"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES += " \
    packagegroup-base-ni-cli \
    packagegroup-devel-ni-cli \
"

RDEPENDS_packagegroup-ni-cli = "\
    packagegroup-base-ni-cli \
    packagegroup-devel-ni-cli \
"

SUMMARY_packagegroup-base-ni-cli = "Packages preinstalled into SmartRacks RCU image"
RRECOMMENDS_packagegroup-base-ni-cli = "\
    vsftpd \
    rauc \
    rcu-hostname \
    coreutils \
    rcu-service \
    udev-ni-rules \
"

SUMMARY_packagegroup-devel-ni-cli = "Tools useful during SmartRacks RCU development"
RRECOMMENDS_packagegroup-devel-ni-cli = "\
    rcu-service-python-test-client \
"
