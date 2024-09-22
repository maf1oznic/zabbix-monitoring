# zabbix-monitoring-aster
## Настройка zabbix-agent
### Создадим папку для пользовательских скриптов в каталоге zabbix:
```
sudo mkdir /etc/zabbix/scripts
```
### Cоздаем скрипт проверки 
```
sudo nano /etc/zabbix/scripts/asterisk.trunk.sh
```
```
#!/bin/sh
# Получаем количество всех транков в системе
number_tranks=`sudo /usr/sbin/asterisk -rx "pjsip show registrations" | grep -c "sip:"`

# Считаем количество зарегистрированных транков
reg_tranks=`sudo /usr/sbin/asterisk -rx "pjsip show registrations" | grep -c "Registered"`

# Вычисляем разницу между полученными значениями
result=$((number_tranks - reg_tranks))

# Выводим результат вычисления
echo $result
```
### Назначаем владельцем файла пользователя zabbix и выставляем права на выполнение скрипта:
```
sudo chown zabbix: /etc/zabbix/scripts/asterisk.trunk.sh
```
```
sudo chmod +x /etc/zabbix/scripts/asterisk.trunk.sh
```
### Изменям sudoers, чтобы zabbix мог выполнять команды с sudo
```
sudo visudo
```
#### Добавить в конец:
```
zabbix ALL = NOPASSWD: /usr/sbin/asterisk
```
### Проверка выполнения скрипта:
```
sudo -u zabbix /etc/zabbix/scripts/asterisk.trunk.sh
```
### Создаем  параметр для заббикса:
```
sudo nano /etc/zabbix/zabbix_agentd.d/aster.conf
```
```
UserParameter=asterisk.trunk,/etc/zabbix/scripts/asterisk.trunk.sh
```
### Перезапуск агента:
```
sudo systemctl restart zabbix-agent
```
### Проверка выполнения:
```
sudo zabbix_agentd -t asterisk.trunk
```
## Импорт шаблона мониторинга на сервере

Data collection --> Templates --> Import
И подсоединяем шаблон к хостам.
Если 3 последние проверки покажут значение, отличное от 0, сработает триггер
