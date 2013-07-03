#!/bin/bash
git pull
sudo cp -v ./go-to-bed-daemon.py /usr/bin/
sudo cp -v ./go-to-bed.py /usr/bin/
sudo cp -v ./go-to-bed-init.sh /etc/init.d/go-to-bed

CONFIG_FILE="/etc/go-to-bed.conf"

if [ ! -f "$CONFIG_FILE" ]
then
    sudo echo "USERS=\"\"" > $CONFIG_FILE
    sudo echo "URL=\"http://localhost/go-to-bed/\"\n" >> $CONFIG_FILE
    echo "$CONFIG_FILE has been created for your convenience."
fi

echo "=== $CONFIG_FILE contents ==="
cat "$CONFIG_FILE"
sudo service go-to-bed stop
sudo service go-to-bed start
sudo update-rc.d go-to-bed defaults
