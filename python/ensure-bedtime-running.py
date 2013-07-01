#!/usr/bin/env python

import subprocess
import re
import pprint
import time
import sys

pp = pprint.PrettyPrinter(indent=4)
session_re = re.compile("(Session[0-9]+)\:")
var_val_re = re.compile("\t(.*)\s\=\s\'(.*)\'")
var_val_bool_re = re.compile("\t(.*)\s\=\s(TRUE|FALSE)")
ps_re = re.compile("(\d+)\s(.*?)\s+(.*)")
ensure_for = ['sam', 'halle']


def exe(cmd, shell=False):
    try:
        return subprocess.check_output(cmd, shell=shell).strip()
    except subprocess.CalledProcessError, e:
        print "subprocess.CalledProcessError %s %s" % (e, cmd)
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
    for l in lines:
        # print "l:",l
        match = ps_re.match(l)
        if match:
            pid, user, cmd = match.groups()
            if user not in ensure_for_users:
                continue
            if cmd.startswith("/usr/bin/python"):
                print pid, user, cmd
                if "go_to_bed.py" in cmd:
                    running_for.append(user)
    return running_for

def start_if_needed():
    ensure_for_users = []
    ck_list_sessions = parse_ck_list_sessions()
    for name, session in ck_list_sessions.items():
        if not session['is-local'] or not session['x11-display']:
            continue
        print "s:",
        pp.pprint(session)
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
        print "starting for:",user
        args = [
            'su',
            '-',
            user['user'],
            '-c',
            "export DISPLAY='%s';/usr/bin/go_to_bed.py --url 'http://the-erm.com/go-to-bed/'" % user['x11-display']
        ]
        subprocess.Popen(args)


if __name__ == "__main__":
    for i, a in enumerate(sys.argv):
        print "i:",i
        print "a:",a
        if a == "--users" && len(sys.argv) > i:
            users = sys.argv[i+1].split(",")
            print "enusre_for:",users
            ensure_for = users

    if "--run-once" in sys.argv:
        start_if_needed()
        sys.exit()
    while True:
        start_if_needed()
        time.sleep(60)
        print ".",
