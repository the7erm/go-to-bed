#!/bin/bash

git pull
sudo cp -v ./go-to-bed-daemon.py /usr/bin/
sudo cp -v ./go-to-bed.py /usr/bin/
sudo cp -v ./go-to-bed-init.sh /etc/init.d/go-to-bed
sudo chmod +x /usr/bin/go-to-bed-daemon.py -c
sudo chmod +x /usr/bin/go-to-bed.py -c
sudo chmod +x /etc/init.d/go-to-bed -c


CONFIG_FILE="/etc/go-to-bed.conf"

if [ ! -f "$CONFIG_FILE" ]
then
    echo "Generating $CONFIG_FILE"
    sudo echo "USERS=\"\"" | sudo tee -a $CONFIG_FILE
    sudo echo "# example:USERS=\"child1login,child2login\" #separate by ," | sudo tee -a $CONFIG_FILE
    
    sudo echo -e "URL=\"http://localhost/go-to-bed/\"\n" | sudo tee -a $CONFIG_FILE
    echo "$CONFIG_FILE has been created for your convenience."
fi

echo "=== $CONFIG_FILE contents ==="
cat "$CONFIG_FILE"
echo -e "\n"
sudo update-rc.d -f go-to-bed remove 
sudo update-rc.d go-to-bed defaults 98 2
sudo service go-to-bed stop
sudo service go-to-bed start
