# Звонок от заббикса на телефон

### Настройка медиа типа
Создаем скрипт запроса на звонок к астериску:
```
nano /usr/lib/zabbix/alertscripts/aster_call.py
```
Создаем медиа тип в заббиксе:


![image](https://github.com/user-attachments/assets/3ca9c340-af2a-4500-ad43-dc2cbda02434)


На сервере астериска создаем скрипт который преобразует текст от заббикса в аудио:
```
sudo nano /opt/asterisk/scripts/gtts_script.py
```

Добавляем мой диалплан:
```
nano /etc/asterisk/extensions/conf
```
