#!/bin/bash

# Project skidloader
# This is the script required for autostarting
# all dependent executables
# and is getting called by rocket.services launcher
# at the boot time

# Author: Martin Shishkov
# Created : 05.03.2020
#
 sleep 5;
 echo "gulliversoft, starting second RIB instance with motion capture priority loop"
 sudo $PWD/RIB_App -c 2 ;
 printf "RIB_App pid: %s\n" "$(pidof RIB_App)" ;
 tail -F /var/log/syslog | grep --line-buffered '(RIB_App/src/main.cpp): Setup server socket complete: 0'|
         {      read line;
                echo $line;
                echo "############# starting motion provider";
                ./motion &
                echo "############# waiting on motion-stream for starting all consumers";
                tail -F /var/log/syslog | grep --line-buffered 'motion_init: Started motion-stream server on ### gulliversoft ### RIB side channel with portforward'|
                {       read line2;
                        echo $line2;
                        echo "############# starting motion consumer";
                        sudo $PWD/Digger_Motion_Consumer_App -l 10 -s 1 ;
                };
                exit 0;
        }
