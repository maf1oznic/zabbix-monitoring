# check-rtsp-cam
## Настройка zabbix-agent
### Создадим папку для пользовательских скриптов в каталоге zabbix:
```
sudo mkdir /etc/zabbix/scripts
```
#### Создадим текстовый файл для хранения url камер. В этот файл необходимо добавить url по одному на каждую строку (пример в текстовике).
```
sudo nano /etc/zabbix/scripts/cameras_rtsp.txt
```
#### Дальше добавляем скрипты для автообнаружения камер и передачи в zabbix.
```
sudo nano /etc/zabbix/scripts/disc_rtsp_cameras.sh
```
```
#!/bin/bash

JSON=$(for line in $(cat /etc/zabbix/scripts/cameras_rtsp.txt); do
    id=$(echo $line | cut -d':' -f1)
    printf "{\"{#CAMERA_ID}\":\"$id\"},"
done | sed 's/^\(.*\).$/\1/')
printf "{\"data\":["
printf "$JSON"
printf "]}"
```
#### Пишем скрипт, который будет проверять доступность потока с камеры.
```
sudo nano /etc/zabbix/scripts/check_rtsp_camera.sh
```
```
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
```
#### Делаем скрипты исполняемыми:
```
sudo chmod +x check_rtsp_camera.sh disc_rtsp_cameras.sh
```
#### Проверить работу скриптов можно вот так:
```
/etc/zabbix/scripts/check_rtsp_camera.sh Camera1
1
```
## Связываем скрипты с самим zabbix.
#### Создаем файл с расширением конфигурации заббикса:
```
sudo nano /etc/zabbix/zabbix_agentd.d/rtsp.conf
```
```
UserParameter=cameras_rtsp.discovery[*],/etc/zabbix/scripts/disc_rtsp_cameras.sh
UserParameter=cameras_rtsp.status[*],/etc/zabbix/scripts/check_rtsp_camera.sh $1
```
#### Делаем пользователя zabbix владельцем всех скриптов.
```
sudo chown -R zabbix: /etc/zabbix/scripts
```
#### Перезапускаем агента:
```
sudo systemctl restart zabbix-agent
```
#### Проверяем, как заббикс агент возвращает параметры для сервера. Должен вывести список камер.
```
zabbix_agentd -t cameras_rtsp.discovery
```
## Настройка zabbix server для мониторинга ssl сертификатов
#### Импортируйте шаблон себе на сервер. Прикрепляйте этот шаблон к тому хосту, где вы настраивали скрипты и zabbix-agent.
