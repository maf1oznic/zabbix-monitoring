# zabbix-monitoring
### Установка Zabbix агента
```
wget https://repo.zabbix.com/zabbix/7.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest+ubuntu24.04_all.deb 
```
```
sudo dpkg -i zabbix-release_latest+ubuntu24.04_all.deb 
```
```
sudo apt update && sudo apt install zabbix-agent

```
Поменять домен, сервер актив и имя хоста:
```
sudo nano /etc/zabbix/zabbix_agentd.conf 
```
```
sudo systemctl restart zabbix-agent
sudo systemctl enable zabbix-agent
sudo systemctl status zabbix-agent
```
