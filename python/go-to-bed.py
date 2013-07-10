#!/usr/bin/env python

import datetime
import pytz
import time
import sys
import subprocess
import os
import pprint

import dateutil.parser

import json
import urllib2
import urllib
from crontab import CronTab

import gtk
import gobject
import logging
import os

logger = logging.getLogger("go-to-bed")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(os.path.expanduser("~/.go-to-bed.log"))
handler.setFormatter(formatter)
logger.addHandler(handler)


class NotifyWindow(gtk.Window):
    def __init__(self, message="", keep_above=True, close_after=None, 
                 full_screen=False, close_on_click=False, decorated=False,
                 stick=True):
        gtk.Window.__init__(self)
        self.set_default_size(600, 400)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_keep_above(keep_above)

        self.eb = gtk.EventBox()
        self.add(self.eb)

        self.vbox_container = gtk.VBox()
        self.eb.add(self.vbox_container)

        self.label = gtk.Label(message)
        self.vbox_container.pack_start(self.label)
        self.set_decorated(decorated)
        if stick:
            self.stick()

        self.show_all()

        if keep_above:
            gobject.timeout_add(1000, self.ensure_above)

        if close_after:
            gobject.timeout_add(10000, self.destroy_window)

        if full_screen:
            self.fullscreen()

        if close_on_click or not close_after:
            self.eb.connect("button_press_event", self.on_button_press_event)


    def on_button_press_event(self, *args, **kwargs):
        print "on_button_press_event:", args, kwargs
        self.destroy()
        gtk.main_quit()

    def destroy_window(self, *args, **kwargs):
        print "destroy_window:", args, kwargs
        self.destroy()
        gtk.main_quit()
        return False


    def ensure_above(self, *args, **kwargs):
        print "ensure_above:", args, kwargs
        self.set_keep_above(True)
        return False

def exe(cmd, shell=False):
    try:
        return subprocess.check_output(cmd, shell=shell).strip()
    except subprocess.CalledProcessError, e:
        print "subprocess.CalledProcessError %s %s" % (e, cmd)
    return ""

def send_logout(w=None):
    print "send_logout"

    if testing:
        print "exiting --test detected"
        sys.exit()

    qdbus = exe(["which", "qdbus"])
    qdbus = subprocess.check_output(["which", "qdbus"]).strip()
    if qdbus:
        exe(["qdbus", "org.kde.ksmserver", "/KSMServer", "logout", "0", "0", "0"])

    xfce4_session_logout = exe(["which", "xfce4-session-logout"])
    if xfce4_session_logout:
        exe(["xfce4-session-logout", "--logout"])

    gnome_session_quit = exe(["which", "gnome-session-quit"])
    if gnome_session_quit:
        exe(["gnome-session-quit", "--logout", "--no-prompt"])

    sys.exit(1)

def connect(url, get={}, post={}):
    data = urllib.urlencode(get)
    full_url = url + '?' + data
    logger.info("full_url:%s", full_url)
    print "full_url:",full_url

    try:
        req = urllib2.Request(full_url)
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print "urllib2.HTTPError:",full_url,' ',e
        return {}
    except urllib2.URLError, e:
        print "urllib2.URLError:",full_url,' ',e
        return {}
    the_page = response.read()
    try:
        res = json.loads(the_page)
    except ValueError, e:
        print "ValueError:",e
        print "Could not decode:",the_page
        return {}

    return res

def check_url():
    values = {'status': os.getenv('USER')}
    if isinstance(testing, str) and not testing.startswith("--"):
        values = {'status': testing}
    
    res = connect(url, values)
    print "res: ",
    pp.pprint(res)
    if not res:
        return
    parse_grounded(res)
    parse_reminders(res)
    parse_restriction(res)
    parse_messages(res, values)

def parse_grounded(res):

    if (not res.has_key('grounded') or not res['grounded'].has_key('until') or
        not isinstance(res['grounded'], dict)):
        return

    date = res['grounded']['until'].get('date','')
    time = res['grounded']['until'].get('time', '')
    message = res['grounded'].get('message', 'There was no message, but you\'re grounded.')

    if not date and not time:
        return

    grounded_until = None
    if date and time:
        grounded_until = datetime.datetime.strptime("%s %s" % (date, time), '%m/%d/%Y %I:%M%p')
    elif date:
        grounded_until = datetime.datetime.strptime(date, '%m/%d/%Y')

    if not grounded_until:
        return
    now = datetime.datetime.now()

    if now >= grounded_until:
        return

    window =  NotifyWindow(message, full_screen=True, close_after=10000)
    gtk.main()
    send_logout()

def parse_messages(res, get):
    # messages
    messages = res.get('messages', {})
    if not isinstance(messages, dict) or not messages:
        return
    get['msg_for'] = get['status']
    del get['status']

    for k, m in res['messages'].iteritems():
        print m
        window =  NotifyWindow(m)
        gtk.main()
        get['id'] = k
        connect(url, get)

def parse_reminders(res):
    if not res.has_key('reminders') or not isinstance(res['reminders'], dict):
        return

    now = datetime.datetime.now()
    for k, r in res['reminders'].iteritems():
        if not r.has_key('cron') or not r['cron']:
            continue

        try:
            r['entry'] = CronTab(r['cron'])
        except ValueError, e:
            print "ValueError: ",e, r['cron']
            continue
        r['next'] = r['entry'].next(now)

        active_crons[k] = r

def parse_restriction(res):
    if not res.has_key('restriction') or not isinstance(res['restriction'], dict):
        return

    now = datetime.datetime.now()
    key = 'school_night'
    if now.strftime("%w") >= 5: # 0=sunday 6=saturday
        key = 'weekend'

    if not res['restriction'].has_key(key):
        return

    rule = res['restriction'][key]

    if not rule.has_key('start') or not rule.has_key('end'):
        return

    pp.pprint(rule)

    start = dateutil.parser.parse(rule['start'])
    end = dateutil.parser.parse(rule['end'])

    if end < start:
        if now < end:
            window = NotifyWindow(rule['message'], 
                                  close_after=10000,
                                  full_screen=True)
            gtk.main()
            send_logout()

        end = end + datetime.timedelta(1)

    if now >= start and now <= end:
        window = NotifyWindow(rule['message'], 
                              close_after=10000,
                              full_screen=True)
        gtk.main()
        send_logout()


def execute_cron(c):
    now = datetime.datetime.now()
    c['next'] = c['entry'].next(now)
    close_after = None
    close_on_click = True
    if c['logout']:
        close_after = 10000
        close_on_click = False


    full_screen = False
    if c['full_screen']:
        full_screen = True

    window =  NotifyWindow(c['message'], close_after=close_after, 
                           full_screen=full_screen)
    gtk.main()
    now = datetime.datetime.now()
    c['next'] = c['entry'].next(now)

    if c['logout']:
        send_logout()
        sys.exit()

    
cnt = 0
url = "http://localhost/go-to-bed/"
pp = pprint.PrettyPrinter(indent=4)
active_crons = {}
testing = False

if "--test" in sys.argv:
    testing = True
    idx = sys.argv.index("--test")
    if len(sys.argv) >= idx:
        testing = sys.argv[idx+1]
    print "testing:",testing

if "--url" in sys.argv:
    _url = ""
    idx = sys.argv.index("--url")
    if len(sys.argv) >= idx:
        _url = sys.argv[idx+1]
    if _url and not _url.startswith("http:") and not _url.startswith("https:"):
        _url = "http://%s" % _url
    url = _url

logger.info("Starting gui client:%s", url)

while True:
    if cnt % 60 == 0:
        cnt = 1
        check_url()

    print "seconds since last check:",cnt
    cnt = cnt + 1

    for k, c in active_crons.items():
        active_crons[k]['next'] -= 1;
        if c['next'] <= 0:
            execute_cron(c)

        if cnt % 10 == 0:
            now = datetime.datetime.now()
            next = c['entry'].next(now)
            active_crons[k]['next'] = next

    time.sleep(1)

