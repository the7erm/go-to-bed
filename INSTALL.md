
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
sudo cp php/* /var/www/go-to-bed/ -Rv
sudo chown www-data:www-data /var/www/go-to-bed -Rc
```

Or system link it.  I system link because I'm developing but for security reasons
it's probably better to copy the files over.

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

Set up the clients on 1 computer
================================
Copy the contents of the python/ folder to /usr/bin/ (or wherever you prefer)
```
sudo cp ./python/* /usr/bin/ -v
sudo chmod +x /usr/bin/go_to_bed.py
cp ./sample.desktop ./sample.desktop.bak
sudo cp ./sample.desktop /home/<child_account>/.config/autostart/go-to-bed.desktop
sudo chmod o-w /home/<child_account>/.config/autostart/go-to-bed.desktop
```

Keep in mind this will not work if your kid is smart.  The script is running as
them.  They can run a ps -Af | grep go_to_bed.py and kill the pid easily enough.
If my kids figure that out.  I'll be happy.  Then I'll figure out a way to run
it as root, and export the DISPLAY=":0", but for now this is good enough.


Set up the clients on multiple computers
----------------------------------------
Nutshell version:
* Copy python/go_to_bed.py to each computer's /usr/bin/ folder.
* Edit sample.desktop and change --url parameter to reflect the ip/hostname
  of whatever machine your apache install is on.
* Copy sample.desktop /home/<child_account>/.config/autostart/go-to-bed.desktop 
  to each of the children's accounts on the computers they use.

If you want more in-depth help than this email me. theerm@gmail.com  I'll write
more docs on it,  but as-is with 0 users.  Going into how to set it up is a
little more than I'd prefer to go into at this time.  Make sure the subject is
something like go-to-bed so I'll notice it.

I lost my password
==================
Usernames and passwords for admins are stored in data/users.data.php.

If you loose you're password you'll have to copy users.data.php to 
users.data.php.bak and start the setup process all over again.

All the time rules are stored in another file, so you won't have to re-add all
the reminders.







