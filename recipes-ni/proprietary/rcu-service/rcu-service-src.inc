# TODO: Point to release branch when it is ready.
# If EXTERNALSRC was specified, it will take precedence of SRC_URI and SRCREV

LICENSE = "Proprietary"
LIC_FILES_CHKSUM = "file://${S}/LICENSE;md5=705b07e5952bd7c88df79f29e927c36d"

SRC_URI = " \
    git://github.com/ni/rcu-service.git;branch=main;protocol=https \
"

# TODO: Assign to a fixed revision after release
SRCREV = "${AUTOREV}"

S = "${WORKDIR}/git"

DEPENDS += " python3-grpcio-tools-native virtual/crypt python3-setuptools-native python3-wheel-native "
RDEPENDS_${PN} += " python3 python3-grpcio "
inherit python3native
inherit python3-dir

FILES:${PN} += "${PYTHON_SITEPACKAGES_DIR}"
