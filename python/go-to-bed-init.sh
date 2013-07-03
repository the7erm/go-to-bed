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
USERS="sam,halle,elijah"
URL="http://the-erm.com/go-to-bed/"

case "$1" in
  start)
    echo "Starting go-to-bed-daemon"
    # Start the daemon 
    python /usr/bin/go-to-bed-daemon.py start --url $URL --users $USERS
    ;;
  stop)
    echo "Stopping go-to-bed-daemon"
    # Stop the daemon
    python /usr/bin/go-to-bed-daemon.py stop
    ;;
  restart)
    echo "Restarting go-to-bed-daemon"
    python /usr/bin/go-to-bed-daemon.py stop
    python /usr/bin/go-to-bed-daemon.py start --url $URL --users $USERS
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/go-to-bed-daemon {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
