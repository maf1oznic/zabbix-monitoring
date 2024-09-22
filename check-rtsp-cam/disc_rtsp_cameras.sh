#!/bin/bash

JSON=$(for line in $(cat /etc/zabbix/scripts/cameras_rtsp.txt); do
    id=$(echo $line | cut -d':' -f1)
    printf "{\"{#CAMERA_ID}\":\"$id\"},"
done | sed 's/^\(.*\).$/\1/')
printf "{\"data\":["
printf "$JSON"
printf "]}"
