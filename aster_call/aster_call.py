#!/usr/bin/python3

import telnetlib
import time
import sys

# Настройки AMI
AMI_HOST = "ip addr"
AMI_PORT = 5038
AMI_USER = "admin"
AMI_PASSWORD = "pwd"

trunk = "trunk_name"

def send_action(action):
    """Отправляет действие на AMI"""
    tn.write(action.encode('utf-8') + b'\n\n')
    time.sleep(0.5)
    return tn.read_very_eager().decode('utf-8')


# Проверяем, что переданы четыре аргумента
if len(sys.argv) < 5:
    print("Usage: aster_call.py <phone_number> <event_status> <event_name> <host_name>")
    sys.exit(1)

# Получаем данные из аргументов командной строки
number = sys.argv[1]  # {ALERT.SENDTO}
event_status = sys.argv[2]  # {EVENT.STATUS}
event_name = sys.argv[3]  # {EVENT.NAME}
host_name = sys.argv[4]    # {HOST.NAME}

# Подключаемся к AMI
tn = telnetlib.Telnet(AMI_HOST, AMI_PORT)
tn.read_until(b"Asterisk Call Manager/")

tn.write(
    b"Action: Login\nUsername: " + AMI_USER.encode('utf-8') + b"\nSecret: " + AMI_PASSWORD.encode('utf-8') + b"\n\n"
)
tn.read_very_eager()

# Формируем запрос на вызов
action = f"""Action: Originate
Channel: Local/s@gtts
Context: gtts-test
Exten: s
Priority: 1
CallerID: {number}
Timeout: 30000
Async: true
Variable: EVENT_STATUS={event_status}
Variable: EVENT_NAME={event_name}
Variable: HOST_NAME={host_name}
Variable: TARGET_NUMBER={number}
Variable: TRUNK={trunk}
"""

# Отправляем действие на Asterisk
response = send_action(action)
print(f"Dialing {number} with status '{event_status}' and event '{event_name}' through {trunk}... Response: {response}")

# Завершаем сессию
tn.write(b"Action: Logoff\n\n")
tn.close()
