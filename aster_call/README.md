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
mkdir -p /opt/asterisk/scripts/
```
```
sudo nano /opt/asterisk/scripts/gtts_script.py
```
```
sudo apt install python3.12-venv
cd /opt/asterisk/scripts/
python3 -m venv myenv
source myenv/bin/activate
pip install gtts
sudo apt update
sudo apt install sox libsox-fmt-mp3
```

Добавляем мой диалплан:
```
nano /etc/asterisk/extensions/conf
```
