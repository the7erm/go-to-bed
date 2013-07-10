#! /bin/bash
# Parts of this script were stolen from
# http://www.gavinj.net/2012/06/building-python-daemon-process.html
# Copyright (c) 2013 My Company.
# All rights reserved.
#
# Author: Eugene R. Miller, 2013
#
# Please send feedback to theerm@gmail.com
#
# /etc/init.d/go-to-bed-init
#
### BEGIN INIT INFO
# Provides:          go-to-bed
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     3 4 5
# Default-Stop:      
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

USERS=""
URL="http://localhost/go-to-bed/"
PYTHON="/usr/bin/python"

if [ -f "/etc/go-to-bed.conf" ]
then
    . /etc/go-to-bed.conf
fi

case "$1" in
  start)
    echo "Starting go-to-bed-daemon"
    # Start the daemon 
    $PYTHON /usr/bin/go-to-bed-daemon.py start --url $URL --users $USERS &>>/tmp/go-to-bed
    ;;
  stop)
    echo "Stopping go-to-bed-daemon"
    # Stop the daemon
    $PYTHON /usr/bin/go-to-bed-daemon.py stop &>>/tmp/go-to-bed
    ;;
  restart)
    echo "Restarting go-to-bed-daemon"
    $PYTHON /usr/bin/go-to-bed-daemon.py stop
    $PYTHON /usr/bin/go-to-bed-daemon.py start --url $URL --users $USERS &>>/tmp/go-to-bed
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/go-to-bed-daemon {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
