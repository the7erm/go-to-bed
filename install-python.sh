#!/bin/bash

sudo apt-get install python-dateutil python-tz python-lockfile \
                     python-daemon python-gtk2 python-pip

sudo pip install Crontab pytz

cd python
./update.sh

echo "You will need to edit /etc/go-to-bed.conf any time you add a new child."
