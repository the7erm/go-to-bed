
This system requires a few things to function properly.

I use apache & php.  You could use php & nginx.  It's up to you.

For your convenience I've created an install script.  Called `install.sh`

This will install all the dependencies needed, and copy over the files 
you need, set up a daemon process that auto starts the notification 
system.

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
sudo cp php/* /var/www/go-to-bed/ -Rv
sudo chown www-data:www-data /var/www/go-to-bed -Rc
```

Or system link it.  I system link because I'm developing but for security
reasons it's probably better to copy the files over.

```
sudo ln -s /<wherever your git is>/git/go-to-bed/php/ /var/www/go-to-bed
sudo chgrp www-data /var/www/go-to-bed -Rc
sudo chmod g+w /var/www/go-to-bed -Rc
```

Setup the server
=================
Start by visiting http://localhost/go-to-bed/

* Enter a username, password & confirmation password.
* Create an additional admin accounts for your spouse.

Add children
============
* Enter a child's name
* Enter the start & end times for school nights and weekends
* Enter a message to be displayed when it's bedtime.
* Click "Create Child Account"
* Repeat process for as many children as you have.


Setup Reminders For Children
============================
You can set up all sorts of fun rules.
For instance Monday-Friday at 7:55 am you can display a message that says 
"Time for school" and automatically log them out.

Here's how to do that:
* Click Every _week_
* Click first -all- in the list.
* Click/Select Monday, Tuesday, Wednesday, Thursday, Friday
* Click second -all- 
* Select 7 (This is military time)
* Click last -all-
* Click/Select 55-59
* Enter a message like "Time for school"
* Check the "Log them out during event box"
* Check display message fullscreen (optional)
* Save.

You're done.
Lather rinse repeat. 

There are lots of fun reminders.  Like at 5pm M-F remind them to do their homework.
Schedule the computer to log them out when they should take a shower.


Ground Them
===========
Enter the end date/time, and a message.  They will be automatically logged out.

Install needed packages for python
==================================
```
sudo apt-get install python-dateutil python-tz python-lockfile \
                     python-daemon python-gtk2 python-pip

sudo pip install Crontab pytz

```

Setup the service / client.
===========================
The config file for the service is `/etc/go-to-bed.conf`
```
USERS="sam,halle,elijah"
URL="http://localhost/go-to-bed/"
```
The USERS variable is the system users you want to enable notifications on.
The URL is the server you want to query for restrictions.

To make things easy I have made an install script `./install-python.sh`

This will install all the needed python libraries, as well as copy the python 
files, and init scripts to the proper location.

If you want to setup on multiple computers you'll need to change the hostname 
`localhost` to whatever the server (where you installed apache & php) ip
is.  If you run `ifconfig` on your server it will give you the ip address.  
It  will be in the `inet addr:` field. (127.0.0.1 is localhost)
It's important to note that the ip address must be static (stays the same) 
otherwise the script will break.  Setting up a static ip address is beyond the 
scope of this document.  There are several techniques you can employ to setup a 
static ip address.  A good place to start is in your router's DHCP reservation 
list.

If you have multiple computers you'll need to install the client on each of 
them.

I lost my password
==================
Usernames and passwords for admins are stored in data/users.data.php.

If you loose you're password you'll have to copy users.data.php to 
users.data.php.bak and start the setup process all over again.

All the time rules are stored in another file, so you won't have to re-add all
the reminders.
