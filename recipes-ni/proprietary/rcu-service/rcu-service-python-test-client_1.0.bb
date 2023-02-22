SUMMARY = "RCU Service Python Test Client"
DESCRIPTION = "Recipe to install RCU Service Python Test Client into RCU image"

require rcu-service-src.inc

do_compile() {
	python3 -m grpc_tools.protoc -I${S} --python_out=${S}/tests/python --grpc_python_out=${S}/tests/python ${S}/rcu-service.proto
}

do_install() {
	install -d ${D}${PYTHON_SITEPACKAGES_DIR}
	install -m 0755 ${S}/tests/python/rcupyclient.py ${D}${PYTHON_SITEPACKAGES_DIR}
	install -m 0755 ${S}/tests/python/rcu_service_pb2.py ${D}${PYTHON_SITEPACKAGES_DIR}
	install -m 0755 ${S}/tests/python/rcu_service_pb2_grpc.py ${D}${PYTHON_SITEPACKAGES_DIR}
	install -m 0755 ${S}/tests/python/example.py ${D}${PYTHON_SITEPACKAGES_DIR}
}
