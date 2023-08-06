#!/bin/bash

# Project skidloader
# This is the script required for autostarting
# all dependent executables
# and is getting called by rocket.services launcher
# at the boot time

# Author: Martin Shishkov
# Created : 05.03.2020
#

 echo "gulliversoft, starting first RIB instance with rc priority loop"
 sudo $PWD/RIB_App -c 2 ;
 printf "RIB_App pid: %s\n" "$(pidof RIB_App)" ;
 tail -F /var/log/syslog | grep --line-buffered '(RIB_App/src/main.cpp): Setup server socket complete: 0'|
	 {	read line;
		echo $line;
		echo "############# starting rocket-daisy and digger consumer";
		python3 -m rocket -c /etc/daisy/config &
		sudo $PWD/Digger_Consumer_App ;
		exit 0 ;
	 }
