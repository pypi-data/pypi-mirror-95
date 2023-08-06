# OPBOT - pure python3 IRC bot (op/obj.py)
#
# This file is placed in the Public Domain.

"objects"

# imports

import datetime, importlib, json, os, random, sys, uuid

# classes

class ENOCLASS(Exception):

    pass

class ENOFILENAME(Exception):

    pass

class O:

    __slots__ = ("__dict__",)

    def __delitem__(self, k):
        try:
            del self.__dict__[k]
        except KeyError:
            pass

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __str__(self):
        return json.dumps(self, default=default, sort_keys=True)

class Object(O):

    __slots__ = ("__id__", "__type__", "__stp__")

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__id__ = str(uuid.uuid4())
        self.__type__ = get_type(self)
        if args:
            self.__dict__.update(args[0])

class Default(Object):

    default = ""

    def __getattr__(self, k):
        try:
            return super().__getattribute__(k)
        except AttributeError:
            try:
                return super().__getitem__(k)
            except KeyError:
                return self.default

class Cfg(Default):

    def op(self, ops):
        for o in ops:
            if o in self.opts:
                return True
        return False

class Ol(Object):

    def append(self, key, value):
        if key not in self:
            self[key] = []
        if isinstance(value, type(list)):
            self[key].extend(value)
        else:
            self[key].append(value)

    def update(self, d):
        for k, v in d.items():
            self.append(k, v)

# functions

def cdir(path):
    if os.path.exists(path):
        return
    res = ""
    path2, _fn = os.path.split(path)
    for p in path2.split(os.sep):
        res += "%s%s" % (p, os.sep)
        padje = os.path.abspath(os.path.normpath(res))
        try:
            os.mkdir(padje)
            os.chmod(padje, 0o700)
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            pass

def get_cls(fullname):
    try:
        modname, clsname = fullname.rsplit(".", 1)
    except Exception as ex:
        raise ENOCLASS(fullname)
    if modname in sys.modules:
        mod = sys.modules[modname]
    else:
        mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def get_type(o):
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    cls = get_cls(cname)
    o = cls()
    load(o, fn)
    return o

def hooked(d):
    return Object(d)

def default(o):
    if isinstance(o, Object):
        return vars(o)
    if isinstance(o, dict):
        return o.items()
    if isinstance(o, list):
        return iter(o)
    if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
        return o
    return repr(o)

def edit(o, setter, skip=False):
    try:
        setter = vars(setter)
    except (TypeError, ValueError):
        pass
    if not setter:
        setter = {}
    count = 0
    for key, value in setter.items():
        if skip and value == "":
            continue
        count += 1
        if value in ["True", "true"]:
            o[key] = True
        elif value in ["False", "false"]:
            o[key] = False
        else:
            o[key] = value
    return count

def format(o, keys=None, skip=None):
    if keys is None:
        keys = vars(o).keys()
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in keys:
        if key in skip:
            continue
        try:
            val = o[key]
        except KeyError:
            continue
        if not val:
            continue
        val = str(val).strip()
        res.append((key, val))
    result = []
    for k, v in res:
        result.append("%s=%s%s" % (k, v, " "))
    txt += " ".join([x.strip() for x in result])
    return txt.strip()

def get(o, k, d=None):
    if isinstance(o, dict):
        return o.get(k, d)
    return o.__dict__.get(k, d)

def items(o):
    try:
        return o.items()
    except (TypeError, AttributeError):
        return o.__dict__.items()

def keys(o):
    try:
        return o.keys()
    except (TypeError, AttributeError):
        return o.__dict__.keys()

def load(o, opath):
    from .run import cfg
    assert opath
    assert cfg.wd
    if opath.count(os.sep) != 3:
        raise ENOFILENAME(opath)
    spl = opath.split(os.sep)
    stp = os.sep.join(spl[-4:])
    lpath = os.path.join(cfg.wd, "store", stp)
    typ = spl[0]
    id = spl[1]
    with open(lpath, "r") as ofile:
        try:
            v = json.load(ofile, object_hook=hooked)
        except json.decoder.JSONDecodeError as ex:
            return
        if v:
            update(o, v)
    o.__id__ = id
    o.__type__ = typ
    o.__stp__ = stp
    return stp

def mkstamp(o):
    timestamp = str(datetime.datetime.now()).split()
    return os.path.join(get_type(o), str(uuid.uuid4()), os.sep.join(timestamp))

def ojson(o, *args, **kwargs):
    return json.dumps(o, default=default, *args, **kwargs)

def register(o, k, v):
    o[k] = v

def save(o, stime=None):
    from .run import cfg
    assert cfg.wd
    if stime:
        stp = os.path.join(o.__type__, o.__id__,
                           stime + "." + str(random.randint(0, 100000)))
    else:
        timestamp = str(datetime.datetime.now()).split()
        stp = os.path.join(o.__type__, o.__id__, os.sep.join(timestamp))
    opath = os.path.join(cfg.wd, "store", stp)
    cdir(opath)
    with open(opath, "w") as ofile:
        json.dump(o, ofile, default=default)
    os.chmod(opath, 0o444)
    o.__stp__ = stp
    return stp

def scan(o, txt):
    for _k, v in items(o):
        if txt in str(v):
            return True
    return False

def set(o, k, v):
    setattr(o, k, v)

def search(o, s):
    ok = False
    for k, v in items(s):
        vv = get(o, k)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok

def update(o, d):
    try:
        return o.__dict__.update(vars(d))
    except TypeError:
        return o.__dict__.update(d)

def values(o):
    try:
        return o.values()
    except (TypeError, AttributeError):
        return o.__dict__.values()

def xdir(o, skip=None):
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res

# runtime

cfg = Cfg()
cfg.wd = ""
