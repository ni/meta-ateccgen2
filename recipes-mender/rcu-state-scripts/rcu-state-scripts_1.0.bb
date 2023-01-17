SUMMARY = "RCU Mender State Scripts"
DESCRIPTION = "Recipe to install RCU Mender State Scripts"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://retain-credentials "

inherit mender-state-scripts

do_compile() {
    cp ${WORKDIR}/retain-credentials ${MENDER_STATE_SCRIPTS_DIR}/ArtifactInstall_Enter_00
}
