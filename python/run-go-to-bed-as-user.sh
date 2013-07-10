#!/bin/bash
DISPLAY=$1
URL=$2
USER=$3
export DISPLAY="$1";
/usr/bin/go-to-bed.py --url "$URL"
echo "run-go-to-bed-as-user.sh DISPLAY:$DISPLAY URL:$URL USER:$USER" &>> /tmp/go-to-bed-start
chmod 666 /tmp/go-to-bed-start
