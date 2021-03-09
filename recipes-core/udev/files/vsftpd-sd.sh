#!/bin/sh
#
# Called from udev
#
# Starts/stops vsftpd.service on SD card hotplug


if [ "$ACTION" = "add" ]; then
	# Start vsftpd.service
	systemctl start vsftpd

elif [ "$ACTION" = "remove" ]; then
	# Stop vsftpd.service
	systemctl stop vsftpd

else
	# Handling edge case if something unexpected happens
	logger "Unknown action: $ACTION triggered"
fi
