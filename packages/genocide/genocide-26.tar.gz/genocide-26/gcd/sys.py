# OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://pypi.org/project/genocide !
#
# This file is placed in the Public Domain.

"system commands"

# imports

import threading, time

from op.obj import Object, get, update
from op.hdl import Bus
from op.prs import elapsed
from op.run import starttime
from op.utl import get_name

# defines

def __dir__():
    return ("flt", "thr", "upt")

# commands

def flt(event):
    try:
        event.reply(str(Bus.objs[event.prs.index]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([get_name(o) for o in Bus.objs]))

def thr(event):
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        update(o, thr)
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = thr.getName()
        if not thrname:
            continue
        if thrname:
            result.append((up, thrname))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s %s" % (txt, elapsed(up)))
    if res:
        event.reply(" | ".join(res))

def upt(event):
    event.reply(elapsed(time.time() - starttime))
