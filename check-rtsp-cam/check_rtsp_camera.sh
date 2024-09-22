#!/bin/bash

CAMERA_ID=$1
CAMERA_URL=$(grep "^$CAMERA_ID:" /etc/zabbix/scripts/cameras_rtsp.txt | cut -d':' -f2-)

# Если URL не найден, вывести ошибку и завершить скрипт
if [ -z "$CAMERA_URL" ]; then
    echo "Error: Camera URL not found for ID $CAMERA_ID"
    exit 1
fi

# Выполнить проверку потока
ffmpeg -hide_banner -loglevel error -i "$CAMERA_URL" -t 1 -f null - 2>/dev/null

# Проверить код выхода ffmpeg
if [ $? -eq 0 ]; then
    echo 1  # Камера доступна
else
    echo 0  # Камера недоступна
fi
