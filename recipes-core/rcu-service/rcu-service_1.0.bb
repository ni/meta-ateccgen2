SUMMARY = "RCU Service"
DESCRIPTION = "Recipe to install RCU Service into RCU image"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit systemd
SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE_${PN} = "rcu-service.service"

# TODO: Point to release branch when it is ready.
# If EXTERNAL_SRC was specified, it will take precedence of SRC_URI and SRC_REV
SRC_URI = "git://github.com/ni/rcu-service.git;branch=main;protocol=https"

# TODO: Assign to a fixed revision after release
SRCREV = "${AUTOREV}"

FILES_${PN} += "${systemd_unitdir}/system/rcu-service.service"
S = "${WORKDIR}/git"
TARGET_CC_ARCH += "${LDFLAGS}"

DEPENDS = " protobuf-native grpc grpc-native "

inherit cmake pkgconfig

# A hacky way to get grpc dependencies to work in order to build RCU service
# Remove grpc installation .cmake files to allow cmake to find grpc-native 
# this allows cmake to find grpc_cpp_plugin
# Then, manually copy five aarch64 .so files required to build RCU service to x86 sysroot

do_configure_prepend() {
         rm -rf ${WORKDIR}/recipe-sysroot/usr/lib/cmake/grpc
         cp ${WORKDIR}/recipe-sysroot/usr/lib/libgrpc++_reflection.so.1.24.3 ${WORKDIR}/recipe-sysroot-native/usr/lib/
         cp ${WORKDIR}/recipe-sysroot/usr/lib/libgrpc++.so.1.24.3 ${WORKDIR}/recipe-sysroot-native/usr/lib/
         cp ${WORKDIR}/recipe-sysroot/usr/lib/libgrpc.so.6.0.0 ${WORKDIR}/recipe-sysroot-native/usr/lib/
         cp ${WORKDIR}/recipe-sysroot/usr/lib/libgpr.so.6.0.0 ${WORKDIR}/recipe-sysroot-native/usr/lib/
         cp ${WORKDIR}/recipe-sysroot/usr/lib/libaddress_sorting.so.6.0.0 ${WORKDIR}/recipe-sysroot-native/usr/lib/
}

do_install() {
         install -d ${D}${bindir}
         install -m 0755 rcu-service ${D}${bindir}
         install -m 0755 rcu-service-cpp-test-client ${D}${bindir}
         install -d ${D}/${systemd_unitdir}/system
         install -m 0644 ${S}/rcu-service.service ${D}/${systemd_unitdir}/system
}

