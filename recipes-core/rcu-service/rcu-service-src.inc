# TODO: Point to release branch when it is ready.
# If EXTERNALSRC was specified, it will take precedence of SRC_URI and SRCREV

SRC_URI = "\
    git://github.com/ni/rcu-service.git;branch=main;protocol=https \
    file://mfgconfig.json \
"
# TODO: Assign to a fixed revision after release
SRCREV = "${AUTOREV}"

S = "${WORKDIR}/git"

DEPENDS += " python3-grpcio-tools-native"
RDEPENDS_${PN} += " python3 python3-grpcio "
inherit python3native
inherit python3-dir

FILES_${PN} += "${PYTHON_SITEPACKAGES_DIR} /data/rcu-service /data/rcu-service/config/*"
