SUMMARY = "NI ATE Core Configurations Gen 2 packagegroups which provide proprietary cmdline releated packages"

PACKAGE_ARCH = "${MACHINE_ARCH}"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES += " \
    packagegroup-base-ni-proprietary-cli \
    packagegroup-devel-ni-proprietary-cli \
"

RDEPENDS:packagegroup-ni-proprietary-cli = "\
    packagegroup-base-ni-proprietary-cli \
    packagegroup-devel-ni-proprietary-cli \
"

SUMMARY:packagegroup-base-ni-proprietary-cli = "Proprietary packages preinstalled into NI ATE Core Configurations Gen 2 RCU image"
RRECOMMENDS:packagegroup-base-ni-proprietary-cli = "\
    rcu-service \
"

SUMMARY:packagegroup-devel-ni-proprietary-cli = "Proprietary tools useful during NI ATE Core Configurations Gen 2 RCU development"
RRECOMMENDS:packagegroup-devel-ni-proprietary-cli = "\
    rcu-service-python-test-client \
"
