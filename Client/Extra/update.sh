#!/bin/bash

cp ../config.py ../config.py.backup

git fetch --all
git reset --hard origin/master

mv ../config.py.backup ../config.py

[ ! -f "/etc/cron.hourly/10submit_temp" ]; ln -s ../submit_temperatures.py /etc/cron.hourly/10submit_temp
[ ! -f "/etc/cron.hourly/11update" ]; ln -s update.sh /etc/cron.hourly/11update

chmod +x ../submit_temperatures.py
chmod +x update.sh
chmod +x startup.sh

if [ "$1" != "-norestart" ]; then
    systemctl restart heatcontroller
fi