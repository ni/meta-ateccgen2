#!/bin/sh
#
# Called from udev
#
# Mount uSD with correct permissions to FTP writable location

if [ "$ACTION" = "add" ]; then
    ftp_uid=$(id -u ftp)
    ftp_gid=$(id -g ftp)

    MOUNT="systemd-mount -o silent -o uid=${ftp_uid},gid=${ftp_gid}"

    if ! $MOUNT --no-block -t auto $DEVNAME "/var/lib/ftp/upload"
    then
        logger "Mount failed failed!"
    else
        logger "Mount successful"
    fi
fi
