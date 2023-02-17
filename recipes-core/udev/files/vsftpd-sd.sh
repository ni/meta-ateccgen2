#!/bin/sh
#
# Called from udev
#
# Starts/stops vsftpd.service on SD card hotplug


if [ "$ACTION" = "add" ]; then
	# Attempt to mount SD card to FTP writable location
	ftp_uid=$(id -u ftp)
	ftp_gid=$(id -g ftp)
	mount -o uid=${ftp_uid},gid=${ftp_gid} /dev/mmcblk1p1 /var/lib/ftp/upload
	retcode=$?
	if [ $retcode -eq 0 ]; then
		logger "Mount success."
		# Attempt to start vsftpd.service if mount success
		systemctl start vsftpd
		retcode=$?
		if [ $retcode -eq 0 ]; then
			logger "vsftpd.service has been started by udev."
		else
			logger "vsftpd.service failed to start with code: " $retcode
		fi
	else
		logger "Mount failed with code: " $retcode
	fi

elif [ "$ACTION" = "remove" ]; then
	# Attempt to stop vsftpd.service
	systemctl stop vsftpd
	retcode=$?
	if [ $retcode -eq 0 ]; then
		logger "vsftpd.service has been stopped by udev."
	else
		logger "vsftpd.service failed to stop with code: " $retcode
	fi
else
	# Handling edge case if something unexpected happens
	logger "Unknown action: $ACTION triggered"
fi
