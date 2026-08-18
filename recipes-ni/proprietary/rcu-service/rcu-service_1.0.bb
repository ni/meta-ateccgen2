SUMMARY = "RCU Service"
DESCRIPTION = "Recipe to install RCU Service into RCU image"

require rcu-service-src.inc
require rcu-service-cpp.inc

SRC_URI += " \
    file://rcu-service-web.py \
    file://rcu-service-web.service \
"

inherit systemd
SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "rcu-service.service rcu-service-web.service"
RDEPENDS_${PN} += " python3 python3-grpcio rcu-service-python-test-client "

do_install() {
         install -d ${D}${bindir}
         install -m 0755 rcu-service ${D}${bindir}
         install -m 0755 ${WORKDIR}/rcu-service-web.py ${D}${bindir}/rcu-service-web.py
         install -d ${D}/${systemd_unitdir}/system
         install -m 0644 ${S}/rcu-service.service ${D}/${systemd_unitdir}/system
         install -m 0644 ${WORKDIR}/rcu-service-web.service ${D}/${systemd_unitdir}/system
         install -d ${D}/${sysconfdir}/ssl/certs
         install -m 0644 ${S}/certs/ni_ate_core_cert.pem ${D}/${sysconfdir}/ssl/certs
}
