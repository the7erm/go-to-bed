#!/bin/sh
while [ "1" = "1" ]
do
    ps -Af | grep go-to-bed | grep -v grep
    sleep 1
done
