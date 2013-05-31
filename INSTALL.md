
This system requires a few things to function properly.

I use apache & php.  You could use php & nginx.  It's up to you.

Install Apache & php
====================
To install apache on a Debian based distro
```
sudo apt-get install apache2 php5
```

* Copy or system link the php folder to a web folder

```
sudo mkdir /var/www/go-to-bed/
sudo chmod 775 /var/www/go-to-bed/
sudo cp php/* /var/www/go-to-bed/
sudo chown www-data:www-data /var/www/go-to-bed -Rc
```

Or system link it.

```
sudo ln -s  /<wherever your git is>/git/go-to-bed/php/ /var/www/go-to-bed
sudo chgrp www-data /<wherever your git is>/git/go-to-bed/php
sudo chmod g+w /<wherever your git is>/git/go-to-bed/php
```

Setting up your sever
=====================


