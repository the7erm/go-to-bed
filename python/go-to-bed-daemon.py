#!/usr/bin/env python
# Parts of this file were blatantly stolen from
# http://www.gavinj.net/2012/06/building-python-daemon-process.html
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import logging
import time
import pprint
import subprocess
import re
import time
import sys
import os
import lockfile
import pipes

#third party libs
from daemon import runner

pp = pprint.PrettyPrinter(indent=4)
session_re = re.compile("(Session[0-9]+)\:")
var_val_re = re.compile("\t(.*)\s\=\s\'(.*)\'")
var_val_bool_re = re.compile("\t(.*)\s\=\s(TRUE|FALSE)")
ps_re = re.compile("(\d+)\s(.*?)\s+(.*)")
ensure_for = ['sam', 'halle', 'elijah']
URL = "http://localhost/go-to-bed/"

subprocesses = []

def exe(cmd, shell=False):
    try:
        return subprocess.check_output(cmd, shell=shell).strip()
    except subprocess.CalledProcessError, e:
        logger.error("subprocess.CalledProcessError %s %s" % (e, cmd))
    return ""

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


def parse_etc_passwd():
    fp = open("/etc/passwd","r")
    user_map = {}
    for l in fp:
        parts = l.split( ":" )
        user_map[parts[2]] = parts[0]

    return user_map

def is_go_to_bed_running(ensure_for_users):
    output = exe(["ps","-Ao","pid,user,cmd"])
    lines = output.split("\n")
    running_for = []
    users = []
    for u in ensure_for_users:
        users.append(u['user'])
    for l in lines:
        match = ps_re.search(l)
        if match:
            pid, user, cmd = match.groups()
            if user not in users:
                continue
            logger.info("checking:%s %s", user, cmd)
            if cmd.startswith("/usr/bin/python") or cmd.startswith('python'):
                logger.info("python:%s", cmd)
                if "go-to-bed.py" in cmd:
                    logger.info("running_for:%s %s", user, cmd)                
                    running_for.append(user)
    return running_for

def start_if_needed():
    ensure_for_users = []
    ck_list_sessions = parse_ck_list_sessions()
    for name, session in ck_list_sessions.items():
        if not session['is-local'] or not session['x11-display']:
            continue
        if session['unix-user'] in ensure_for:
            ensure_for_users.append({
                'user': session['unix-user'],
                'x11-display': session['x11-display']
            })

    if not ensure_for_users:
        return

    # ensure_for_users = set(ensure_for_users)
    is_running_for = is_go_to_bed_running(ensure_for_users)
    for user in ensure_for_users:
        if user['user'] in is_running_for:
            logger.info("Already running for: %s", user)
            continue
        logger.info("starting for: %s", user)
        args = [
            'su',
            '-',
            user['user'],
            '-c',
            "/usr/bin/run-go-to-bed-as-user.sh %s %s %s" % (
                pipes.quote(user['x11-display']),
                pipes.quote(URL),
                pipes.quote(user['user'])
            )
        ]
        logger.info("args:%s", args)

        
        dev_null = open("/dev/null","rw")
        subprocesses.append(
            subprocess.Popen(args, stdin=dev_null, 
                               stdout=dev_null, 
                               stderr=dev_null)
        )

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path =  '/var/run/go-to-bed.pid'
        self.pidfile_timeout = 5
            
    def run(self):
        while True:
            #Main code goes here ...
            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
            start_if_needed()
            """
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warn("Warning message")
            logger.error("Error message")
            """
            time.sleep(60)

    def shutdown(self):
        """Overrides Daemon().shutdown() with some clean up"""
        print "Stopping Daemon!"
        for p in subprocesses:
            print "killing:", p.kill()


if __name__ == "__main__":
    logger = logging.getLogger("go-to-bed")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler("/var/log/go-to-bed.log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("Starting")

    for i, a in enumerate(sys.argv):
        if a == "--users" and len(sys.argv) > i:
            users = sys.argv[i+1].split(",")
            for i, u in enumerate(users):
                users[i] = u.strip()

            print "enusre_for:",users
            ensure_for = users
            
        if a == "--url" and len(sys.argv) > i:
            URL = sys.argv[i+1]
            print "URL:",URL
            

    logger.info("go-to-bed gui client will start for users:%s", ensure_for)
    logger.info("go-to-bed will query the url:%s", URL)


    if "--run-once" in sys.argv:
        start_if_needed()
        sys.exit()

    app = App()

    daemon_runner = runner.DaemonRunner(app)
    #This ensures that the logger file handle does not get closed during daemonization
    daemon_runner.daemon_context.files_preserve=[handler.stream]
    daemon_runner.do_action()
    logger.info("Started")
