SUMMARY = "NI ATE Core Configurations Gen 2 packagegroups which provide cmdline releated packages"

PACKAGE_ARCH = "${MACHINE_ARCH}"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES += " \
    packagegroup-base-ni-cli \
    packagegroup-devel-ni-cli \
"

RDEPENDS:packagegroup-ni-cli = "\
    packagegroup-base-ni-cli \
    packagegroup-devel-ni-cli \
"

SUMMARY_packagegroup-base-ni-cli = "Packages preinstalled into NI ATE Core Configurations Gen 2 RCU image"
RRECOMMENDS:packagegroup-base-ni-cli = "\
    vsftpd \
    rcu-hostname \
    coreutils \
    rcu-image-version \
    rcu-state-scripts \
    udev-ni-rules \
    keyutils \
    cifs-utils \
    rcu-config \
    jq \
"

SUMMARY_packagegroup-devel-ni-cli = "Tools useful during NI ATE Core Configurations Gen 2 RCU development"
RRECOMMENDS:packagegroup-devel-ni-cli = "\
    gdb \
"
