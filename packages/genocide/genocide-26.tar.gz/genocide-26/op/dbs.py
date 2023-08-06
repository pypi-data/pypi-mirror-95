# OPBOT - pure python3 IRC bot (op/dbs.py)
#
# This file is placed in the Public Domain.

"database"

# imports

from .obj import get_type, hook, search, update, os
from .run import cfg
from .utl import fntime

# defines

def __dir__():
    return ("all", "deleted", "every", "find", "find_event", "fnd", "last", "last_match", "last_type", "last_fn")

# functions

def all(otype, selector=None, index=None, timed=None):
    nr = -1
    if selector is None:
        selector = {}
    for fn in fns(otype, timed):
        o = hook(fn)
        if selector and not search(o, selector):
            continue
        if "_deleted" in o and o._deleted:
            continue
        nr += 1
        if index is not None and nr != index:
            continue
        yield fn, o

def deleted(otype):
    for fn in fns(otype):
        o = hook(fn)
        if "_deleted" not in o or not o._deleted:
            continue
        yield fn, o

def every(selector=None, index=None, timed=None):
    nr = -1
    if selector is None:
        selector = {}
    for otype in os.listdir(os.path.join(cfg.wd, "store")):
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

def find(otype, selector=None, index=None, timed=None):
    nr = -1
    if selector is None:
        selector = {}
    for fn in fns(otype, timed):
        o = hook(fn)
        if selector and not search(o, selector):
            continue
        if "_deleted" in o and o._deleted:
            continue
        nr += 1
        if index is not None and nr != index:
            continue
        o.__type__ = otype
        yield fn, o

def find_event(e):
    nr = -1
    for fn in fns(e.otype, e.timed):
        o = hook(fn)
        if e.gets and not search(o, e.gets):
            continue
        if "_deleted" in o and o._deleted:
            continue
        nr += 1
        if e.index is not None and nr != e.index:
            continue
        yield fn, o

def fns(name, timed=None):
    if not name:
        return []
    p = os.path.join(cfg.wd, "store", name) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if timed and "from" in timed and timed["from"] and fntime(p) < timed["from"]:
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)

def last(o):
    path, l = last_fn(str(get_type(o)))
    if  l:
        update(o, l)
    if path:
        spl = path.split(os.sep)
        stp = os.sep.join(spl[-4:])
        return stp

def last_match(otype, selector=None, index=None, timed=None):
    for fn, o in find(otype, selector, index, timed):
        yield fn, o
        break

def last_type(otype):
    fnn = fns(otype)
    if fnn:
        return hook(fnn[-1])

def last_fn(otype):
    fn = fns(otype)
    if fn:
        fnn = fn[-1]
        return (fnn, hook(fnn))
    return (None, None)

def list_files(wd):
    path = os.path.join(wd, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))
