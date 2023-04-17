SUMMARY = "RCU Mender State Scripts"
DESCRIPTION = "Recipe to install RCU Mender State Scripts"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = " \
    file://retain-credentials \
    file://retain-ssh-service-status \
    file://retain-ssl-private-keys \
    file://retain-dbus-machine-id \
"

inherit mender-state-scripts

do_compile() {
    cp ${WORKDIR}/retain-credentials ${MENDER_STATE_SCRIPTS_DIR}/ArtifactInstall_Enter_00
    cp ${WORKDIR}/retain-ssh-service-status ${MENDER_STATE_SCRIPTS_DIR}/ArtifactInstall_Enter_01
    cp ${WORKDIR}/retain-ssl-private-keys ${MENDER_STATE_SCRIPTS_DIR}/ArtifactInstall_Enter_02
    cp ${WORKDIR}/retain-dbus-machine-id ${MENDER_STATE_SCRIPTS_DIR}/ArtifactInstall_Enter_03
}
