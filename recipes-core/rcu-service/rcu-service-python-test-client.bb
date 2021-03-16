SUMMARY = "RCU Service Python Test Client"
DESCRIPTION = "Recipe to install RCU Service Python Test Client into RCU image"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

DEPENDS += " python3-grpcio-tools-native"
inherit python3native

do_compile()
{
	python3 -m grpc_tools.protoc -I${S} --python_out=${S}/tests --grpc_python_out=${S}/tests ${S}/rcu-service.proto
}

do_install()
{
	install -d ${D}${bindir}
	install -m 0755 ${S}/tests/rcu-service-python-test-client.py ${D}${bindir}
}
