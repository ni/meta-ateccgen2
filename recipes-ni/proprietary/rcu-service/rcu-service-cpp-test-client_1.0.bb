SUMMARY = "RCU Service CPP Test Client"
DESCRIPTION = "Recipe to install RCU Service CPP Test Client into RCU image"

require rcu-service-src.inc
require rcu-service-cpp.inc

do_install() {
         install -d ${D}${bindir}
         install -m 0755 rcu-service-cpp-test-client ${D}${bindir}
}
