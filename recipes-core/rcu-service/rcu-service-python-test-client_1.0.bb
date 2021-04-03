SUMMARY = "RCU Service Python Test Client"
DESCRIPTION = "Recipe to install RCU Service Python Test Client into RCU image"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

require rcu-service-src.inc

DEPENDS += " python3-grpcio-tools-native"
RDEPENDS_${PN} += " python3 python3-grpcio "
inherit python3native

do_compile() {
	python3 -m grpc_tools.protoc -I${S} --python_out=${S}/tests/python --grpc_python_out=${S}/tests/python ${S}/rcu-service.proto
}

do_install() {
	install -d ${D}${bindir}
	install -m 0755 ${S}/tests/python/rcu-service-python-test-client.py ${D}${bindir}
	install -m 0755 ${S}/tests/python/rcu_service_pb2.py ${D}${bindir}
	install -m 0755 ${S}/tests/python/rcu_service_pb2_grpc.py ${D}${bindir}
}