SUMMARY = "RCU Service CPP Test Client"
DESCRIPTION = "Recipe to install RCU Service CPP Test Client into RCU image"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

require rcu-service-src.inc
require rcu-service-cpp.inc

do_install() {
         install -d ${D}${bindir}
         install -m 0755 rcu-service-cpp-test-client ${D}${bindir}
}
