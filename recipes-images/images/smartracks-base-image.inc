inherit core-image

LICENSE = "MIT"

#Prefix to the resulting deployable tarball name
export IMAGE_BASENAME = "RCU-Image"
MACHINE_NAME = "NI-ATE-Core"
VERSION = "custom"
IMAGE_NAME = "${MACHINE_NAME}_${IMAGE_BASENAME}_${VERSION}"

# Copy Licenses to image /usr/share/common-license
COPY_LIC_MANIFEST ?= "1"
COPY_LIC_DIRS ?= "1"

# Configure base image root account default password
inherit extrausers
EXTRA_USERS_PARAMS = "usermod -P ni root;"

add_rootfs_version () {
    printf "${DISTRO_NAME} ${DISTRO_VERSION} (${DISTRO_CODENAME}) \\\n \\\l\n" > ${IMAGE_ROOTFS}/etc/issue
    printf "${DISTRO_NAME} ${DISTRO_VERSION} (${DISTRO_CODENAME}) %%h\n" > ${IMAGE_ROOTFS}/etc/issue.net
    printf "${IMAGE_NAME}\n\n" >> ${IMAGE_ROOTFS}/etc/issue
    printf "${IMAGE_NAME}\n\n" >> ${IMAGE_ROOTFS}/etc/issue.net
}
# add the rootfs version to the welcome banner
ROOTFS_POSTPROCESS_COMMAND += " add_rootfs_version;"

IMAGE_LINGUAS = "en-us"
#IMAGE_LINGUAS = "de-de fr-fr en-gb en-us pt-br es-es kn-in ml-in ta-in"

# Remove conflicting packages recommended by packagegroup-base-tdx-cli
BAD_RECOMMENDATIONS = "set-hostname udev-toradex-rules"

IMAGE_INSTALL += " \
    packagegroup-boot \
    packagegroup-basic \
    packagegroup-base-tdx-cli \
    packagegroup-machine-tdx-cli \
    udev-extraconf \
    ${@bb.utils.contains('DISTRO_FEATURES', 'systemd', 'timestamp-service systemd-analyze', '', d)} \
"

# Required to append protobuf and grpc dependencies to SDK
TOOLCHAIN_HOST_TASK_append += " nativesdk-protobuf-compiler nativesdk-grpc-dev nativesdk-python3-grpcio-tools nativesdk-make "
TOOLCHAIN_TARGET_TASK_append += " python3-grpcio-tools "
