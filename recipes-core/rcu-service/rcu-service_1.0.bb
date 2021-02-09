SUMMARY = "RCU Service"
DESCRIPTION = "Recipe to install RCU Service into RCU image"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit systemd
SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE_${PN} = "rcu-service.service"

# TODO: Point to release branch when it is ready.
# If EXTERNAL_SRC was specified, it will take precedence of SRC_URI and SRC_REV
SRC_URI = "git://github.com/ni/rcu-service.git;branch=main"

# TODO: Assign to a fixed revision after release
SRCREV = "${AUTOREV}"

FILES_${PN} += "${systemd_unitdir}/system/rcu-service.service"
S = "${WORKDIR}/git"
TARGET_CC_ARCH += "${LDFLAGS}"

do_compile() {
         ${CXX} ${S}/rcu-service.cpp -o rcu-service
}

do_install() {
         install -d ${D}${bindir}
         install -m 0755 rcu-service ${D}${bindir}
         install -d ${D}/${systemd_unitdir}/system
         install -m 0644 ${S}/rcu-service.service ${D}/${systemd_unitdir}/system
}
