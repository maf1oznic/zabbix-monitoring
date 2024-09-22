# zabbix-monitoring-ssl
## Настройка zabbix-agent
#### Создаем папку для скриптов в директории с настройками zabbix:
```
sudo mkdir /etc/zabbix/scripts
```
#### Создадим текстовый файл для хранения списков доменов.
```
sudo touch /etc/zabbix/scripts/ssl_https.txt
```
#### В этот файл необходимо добавить домены по одному на каждую строку. Дальше добавляем скрипты для автообнаружения этих доменов и передачи в zabbix.
```
sudo nano /etc/zabbix/scripts/disc_ssl_https.sh
```
```
#!/bin/bash

JSON=$(for i in `cat /etc/zabbix/scripts/ssl_https.txt`; do printf "{\"{#DOMAIN_HTTPS}\":\"$i\"},"; done | sed 's/^\(.*\).$/\1/')
printf "{\"data\":["
printf "$JSON"
printf "]}"
```
#### Пишем скрипт, который будет определять, сколько дней осталось до окончания срока действия сертификата.
```
sudo nano /etc/zabbix/scripts/check_ssl_https.sh
```
```
#!/bin/bash

SERVER=$1
TIMEOUT=25
RETVAL=0
TIMESTAMP=`echo | date`
EXPIRE_DATE=`echo | openssl s_client -connect $SERVER:443 -servername $SERVER -tlsextdebug 2>/dev/null | openssl x509 -noout -dates 2>/dev/null | grep notAfter | cut -d'=' -f2`
EXPIRE_SECS=`date -d "${EXPIRE_DATE}" +%s`
EXPIRE_TIME=$(( ${EXPIRE_SECS} - `date +%s` ))
if test $EXPIRE_TIME -lt 0
then
RETVAL=0
else
RETVAL=$(( ${EXPIRE_TIME} / 24 / 3600 ))
fi

echo ${RETVAL}
```
#### Делаем скрипты исполняемыми:
```
cd /etc/zabbix/scripts
sudo chmod +x disc_ssl_https.sh check_ssl_https.sh
```
#### Проверить работу скриптов можно вот так:
```
/etc/zabbix/scripts/check_ssl_https.sh serveradmin.ru
66
/etc/zabbix/scripts/check_ssl_smtp.sh mail.zeroxzed.ru
87
```
## Связываем скрипты с самим zabbix.
#### Создаем файл с расширением конфигурации заббикса:
```
sudo nano /etc/zabbix/zabbix_agentd.d/ssl.conf
```
```
UserParameter=ssl_https.discovery[*],/etc/zabbix/scripts/disc_ssl_https.sh
UserParameter=ssl_https.expire[*],/etc/zabbix/scripts/check_ssl_https.sh $1
```
#### Делаем пользователя zabbix владельцем всех скриптов.
```
chown -R zabbix. /etc/zabbix/scripts
```
#### Перезапускаем агента:
```
sudo systemctl restart zabbix-agent
```
#### Проверяем, как заббикс агент возвращает параметры для сервера. Важный этап перед тем, как приступать к настройке самого сервера.
```
zabbix_agentd -t ssl_https.discovery
```
``
ssl_https.discovery [t|{"data":[{"{#DOMAIN_HTTPS}":"serveradmin.ru"}]}]
``
```
zabbix_agentd -t ssl_https.expire[serveradmin.ru]
```
``
ssl_https.expire[serveradmin.ru] [t|66]
``
## Настройка zabbix server для мониторинга ssl сертификатов
#### Импортируйте шаблон себе на сервер. Прикрепляйте этот шаблон к тому хосту, где вы настраивали скрипты и zabbix-agent. Дальше вам остается только подождать примерно 5 минут. Такой интервал установлен для автообнаружения. Тригеры настроены на 1, 5, 10, 15 и 20 дней.
## [Источник](https://serveradmin.ru/monitoring-sroka-deystviya-ssl-sertifikata-v-zabbix/)
