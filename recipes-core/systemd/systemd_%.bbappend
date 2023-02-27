LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://eth0.network \
    file://eth1.network \
"

PACKAGECONFIG:append = " networkd"

do_install:append() {

    # We install actual eth0 and eth1 network configuration files into persistent data partition
    # allowing these settings to persist across Mender updates
    install -d ${D}/data/systemd/network/
    install -d ${D}/etc/systemd/network/
    install -m 0644 ${WORKDIR}/eth0.network ${D}/data/systemd/network
    install -m 0644 ${WORKDIR}/eth1.network ${D}/data/systemd/network

    # Create symlinks in /etc/systemd/network which point to those files in /data
    ln -s -r ${D}/data/systemd/network/eth0.network ${D}/etc/systemd/network/eth0.network
    ln -s -r ${D}/data/systemd/network/eth1.network ${D}/etc/systemd/network/eth1.network
}

FILES_${PN} += " \
    /data/systemd/network/* \
"
