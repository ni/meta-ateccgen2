SUMMARY = "HelloWorld Application"
DESCRIPTION = "Recipe created by bitbake-layers"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit systemd
SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE_${PN} = "hello.service"

SRCREV = "${AUTOREV}"
SRC_URI = "git://github.com/NI-SmartRack/rcu-software.git;branch=main"
FILES_${PN} += "${systemd_unitdir}/system/hello.service"
S = "${WORKDIR}/git"
TARGET_CC_ARCH += "${LDFLAGS}"

do_compile() {
         ${CXX} hello.cpp -o hello
}

do_install() {
         install -d ${D}${bindir}
         install -m 0755 hello ${D}${bindir}
         install -d ${D}/${systemd_unitdir}/system
         install -m 0644 ${WORKDIR}/git/hello.service ${D}/${systemd_unitdir}/system
}
