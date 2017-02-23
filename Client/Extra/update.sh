#!/bin/bash

cp ../config.py ../config.py.backup
cp heatcontroller.service heatcontroller.service.backup

currentCommit=$(git rev-parse HEAD)

git fetch --all
git reset --hard origin/master

mv ../config.py.backup ../config.py
mv heatcontroller.service.backup heatcontroller.service

if [ "$currentCommit" != "$(git rev-parse HEAD)" ]; then
    exec ./update.sh
fi

chmod +x ../submit_temperatures.py
chmod +x update.sh
chmod +x startup.sh

rm "/etc/cron.hourly/10submit_temp"; ln -s "$(pwd)/../submit_temperatures.py" /etc/cron.hourly/10submit_temp
rm "/etc/cron.hourly/11update"; ln -s "$(pwd)/update.sh" /etc/cron.hourly/11update
rm "/etc/systemd/system/heatcontroller.service"; ln -s "$(pwd)/heatcontroller.service" /etc/systemd/system/heatcontroller.service

systemctl daemon-reload

if [ "$1" != "-norestart" ]; then
    systemctl restart heatcontroller
fi