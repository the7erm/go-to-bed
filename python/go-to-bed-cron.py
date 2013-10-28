#!/usr/bin/env python
import subprocess
import pprint
import re
import os

pp = pprint.PrettyPrinter(indent=4)
session_re = re.compile("(Session[0-9]+)\:")
var_val_re = re.compile("\t(.*)\s\=\s\'(.*)\'")
var_val_bool_re = re.compile("\t(.*)\s\=\s(TRUE|FALSE)")
ps_re = re.compile("(\d+)\s(.*?)\s+(.*)")
ensure_for = ['sam', 'halle', 'elijah']

def exe(cmd, shell=False):
    try:
        return subprocess.check_output(cmd, shell=shell).strip()
    except subprocess.CalledProcessError, e:
        # logger.error("subprocess.CalledProcessError %s %s" % (e, cmd))
        pass
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
        output = exe(['/usr/bin/ck-list-sessions'])
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

xsessions = parse_ck_list_sessions()
dms = [
    '/etc/init.d/kdm',
    '/etc/init.d/lightdm',
    '/etc/init.d/gdm'
]
print xsessions
fp = open("/tmp/go-to-bed-cron", "w")
fp.write("%s\n" % pprint.pformat(xsessions))
for x in xsessions:
    s = xsessions[x]
    print "s:",s
    if s['unix-user'] in ('sam', 'halle'):
        for dm in dms:
            if os.path.exists(dm):
                fp.write("exists:%s\n" % dm)
                basename = os.path.basename(dm)
                fp.write("basename:%s\n" % basename)
                cmd = "/bin/ps -Af | /bin/grep %s | /bin/grep -v grep" % (basename,)
                fp.write("cmd:%s\n" % cmd)
                is_running = exe(cmd, shell=True)
                if is_running:
                    fp.write("running:%s\n" % is_running)
                    cmd = "/usr/sbin/service %s stop" % (basename,)
                    fp.write("cmd:%s\n" % cmd)
                    output = exe(cmd, shell=True)
                    fp.write("output:%s\n", output)
                    cmd = "/usr/sbin/service %s start" % (basename,)
                    fp.write("cmd:%s\n" % cmd)
                    output = exe(cmd, shell=True)
                    fp.write("output:%s\n", output)
                else:
                    fp.write("!running %s\n", (basename,))

fp.close()
