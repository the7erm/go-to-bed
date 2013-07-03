#!/bin/bash

sudo apt-get install apache2 php5
sudo mkdir -p /var/www/go-to-bed/
sudo chmod 775 /var/www/go-to-bed/
sudo cp php/* /var/www/go-to-bed/ -Rv
sudo chown www-data:www-data /var/www/go-to-bed -Rc

echo "go-to-bed web interface has been installed"
echo "visit http://localhost/go-to-bed/ to get started"

