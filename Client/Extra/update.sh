#!/bin/bash

cp ../config.py ../config.py.backup

git fetch --all
git reset --hard origin/master

mv ../config.py.backup ../config.py

chmod +x ../submit_temperatures.py
chmod +x update.sh
chmod +x startup.sh

[ ! -f "/etc/cron.hourly/10submit_temp" ] && ln -s "$(cwd)/../submit_temperatures.py" /etc/cron.hourly/10submit_temp
[ ! -f "/etc/cron.hourly/11update" ] && ln -s "$(cwd)/update.sh" /etc/cron.hourly/11update

if [ "$1" != "-norestart" ]; then
    systemctl restart heatcontroller
fi