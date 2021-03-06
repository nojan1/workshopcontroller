#!/bin/bash

echo "Backing up files"
cp ../config.py ../config.py.backup

currentCommit=$(git rev-parse HEAD)

git fetch --all
git reset --hard origin/master

echo "Restoring files"
mv ../config.py.backup ../config.py

echo "Setting paths for service"
path=$(pwd)
sed -i "s|<WORKPATH>|$path|" heatcontroller.service
sed -i "s|<EXECSTART>|$path/startup.sh|" heatcontroller.service

echo "Setting executable bits"
chmod +x ../submit_temperatures.py
chmod +x update.sh
chmod +x startup.sh

if [ "$currentCommit" != "$(git rev-parse HEAD)" ]; then
    echo "HEAD changed, restarting update"

    if [ "$1" == "-norestart" ]; then
        exec ./update.sh
    else
        exec ./update.sh -restart
    fi
fi

echo "Recreating symlinks"
rm "/etc/cron.hourly/10submit_temp"; ln -s "$(pwd)/../submit_temperatures.py" /etc/cron.hourly/10submit_temp
rm "/etc/cron.hourly/11update"; ln -s "$(pwd)/update.sh" /etc/cron.hourly/11update
rm "/etc/systemd/system/heatcontroller.service"; ln -s "$(pwd)/heatcontroller.service" /etc/systemd/system/heatcontroller.service

echo "Reloading daemons"
systemctl daemon-reload

if [ "$1" == "-restart" ]; then
    echo "Restarting heatcontroller service"
    systemctl restart heatcontroller
fi