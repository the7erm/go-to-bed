#!/usr/bin/env python

import datetime
import pytz
import time
import sys
import subprocess
import os
import pprint
import re
import pwd

import dateutil.parser

import json
import urllib2
import urllib
from crontab import CronTab

import gtk
import gobject
import logging

from logging.handlers import TimedRotatingFileHandler



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
        logger.info("on_button_press_event:%s, %s", args, kwargs)
        self.destroy()
        gtk.main_quit()

    def destroy_window(self, *args, **kwargs):
        logger.info("destroy_window:%s %s", args, kwargs)
        self.destroy()
        gtk.main_quit()
        return False


    def ensure_above(self, *args, **kwargs):
        logger.info("ensure_above:%s %s", args, kwargs)
        self.set_keep_above(True)
        return False

def exe(cmd, shell=False):
    try:
        return subprocess.check_output(cmd, shell=shell).strip()
    except subprocess.CalledProcessError, e:
        logger.error("subprocess.CalledProcessError:%s %s", e, cmd)
    return ""

def send_logout(w=None):
    logger.info("send_logout")

    if testing:
        logger.info("exiting --test detected")
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
    try:
        req = urllib2.Request(full_url)
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        logger.error("urllib2.HTTPError:%s %s", full_url, e)
        return {}
    except urllib2.URLError, e:
        logger.error("urllib2.URLError:%s %s", full_url, e)
        return {}
    the_page = response.read()
    try:
        res = json.loads(the_page)
    except ValueError, e:
        logger.error("ValueError:%s",e)
        logger.error("Could not decode:%s",the_page)
        return {}

    return res

def check_url():
    values = {'status': os.getenv('USER')}
    if isinstance(testing, str) and not testing.startswith("--"):
        values = {'status': testing}
    
    res = connect(url, values)
    logger.info("res:%s",pp.pformat(res))
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
        logger.info("m:%s",m)
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
            logger.error("ValueError:%s %s", e, r['cron'])
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

    logger.info("%s", pp.pformat(rule))

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

def exe(cmd, shell=False):
    try:
        return subprocess.check_output(cmd, shell=shell).strip()
    except subprocess.CalledProcessError, e:
        logger.error("subprocess.CalledProcessError %s %s" % (e, cmd))
    return ""

def parse_etc_passwd():
    fp = open("/etc/passwd","r")
    user_map = {}
    for l in fp:
        parts = l.split( ":" )
        user_map[parts[2]] = parts[0]

    return user_map

def parse_ck_list_sessions():
    users = parse_etc_passwd()
    try:
        output = exe(['ck-list-sessions'])
    except:
        return {}
    lines = output.split("\n")
    session_name = ""
    sessions = {}
    for l in lines:
        match_session = session_re.match(l)
        if match_session:
            session_name = match_session.group(1)
            sessions[session_name] = {}
            continue
        match = var_val_re.search(l)
        is_bool = False
        if match is None:
            match = var_val_bool_re.search(l)
            if match is not None:
                is_bool = True
        if match is None:
            continue
        key = match.group(1)
        value = match.group(2)
        if is_bool:
            if value == "TRUE":
                value = True
            if value == "FALSE":
                value = False

        if key == 'unix-user':
            key = 'unix-uid'

        sessions[session_name][key] = value

        if key == 'unix-uid':
            sessions[session_name]['unix-user'] = users[value]

    return sessions


def set_display(user):
    display = ":0"
    ck_list_sessions = parse_ck_list_sessions()
    for name, session in ck_list_sessions.items():
        if not session['is-local'] or not session['x11-display']:
            continue
        if session['unix-user'] == user:
            display = session['unix-user']
            logger.info("display:%s", display)
    os.putenv('DISPLAY', display)
    os.environ['DISPLAY'] = display

def set_user(uid):
    if uid.isdigit():
        uid = int(uid)
        uinfo = pwd.getpwuid(uid)
    else:
        uinfo = pwd.getpwnam(uid)

    user, pw, uid, gid, gecos, home, shell = uinfo
    set_display(user)
    if os.getuid() != 0:
        logger.error("User must be root to change uid/gid")
        return

    os.putenv('USER', user)
    os.putenv('SHELL', shell)
    os.putenv('HOME', home)
    os.setgid(gid)
    os.setuid(uid)
    os.environ['HOME'] = home
    os.environ['SHELL'] = shell
    os.environ['USER'] = user
    os.environ['USERNAME'] = user
    os.environ['UID'] = "%s" % uid
    os.environ['GID'] = "%s" % gid
    

cnt = 0
url = "http://localhost/go-to-bed/"
pp = pprint.PrettyPrinter(indent=4)
active_crons = {}
testing = False
logger = logging.getLogger("go-to-bed")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler(os.path.expanduser("~/.go-to-bed.log"), 
                                   when="midnight",
                                   backupCount=20)
handler.setFormatter(formatter)
logger.addHandler(handler)
session_re = re.compile("(Session[0-9]+)\:")
var_val_re = re.compile("\t(.*)\s\=\s\'(.*)\'")
var_val_bool_re = re.compile("\t(.*)\s\=\s(TRUE|FALSE)")
ps_re = re.compile("(\d+)\s(.*?)\s+(.*)")

if "--test" in sys.argv:
    testing = True
    idx = sys.argv.index("--test")
    if len(sys.argv) > idx+1:
        testing = sys.argv[idx+1]
    logger.info("testing:%s", testing)

if "--url" in sys.argv:
    _url = ""
    idx = sys.argv.index("--url")
    if len(sys.argv) > idx+1:
        _url = sys.argv[idx+1]
    if _url and not _url.startswith("http:") and not _url.startswith("https:"):
        _url = "http://%s" % _url
    url = _url

if "--uid" in sys.argv:
    idx = sys.argv.index("--uid")
    if len(sys.argv) > idx+1:
        uid = sys.argv[idx+1]
        set_user(uid)

if "--user" in sys.argv:
    idx = sys.argv.index("--user")
    if len(sys.argv) > idx:
        uid = sys.argv[idx+1]
        set_user(uid)


logger.info("Starting gui client:%s", url)

while True:
    if cnt % 60 == 0:
        cnt = 1
        check_url()
    logger.info("seconds since last check:%s", cnt)
    cnt = cnt + 1

    for k, c in active_crons.items():
        active_crons[k]['next'] -= 1;
        if c['next'] <= 0:
            execute_cron(c)

        if cnt % 10 == 0:
            now = datetime.datetime.now()
            next = c['entry'].next(now)
            active_crons[k]['next'] = next
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(1)

