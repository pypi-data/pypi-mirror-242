# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,W0702


"runtime"


import getpass
import os
import time
import _thread


from .msg import Message
from .obj import Default
from .prs import parse
from .rct import CLI
from .dsk import Storage
from .thr import launch
from .utl import spl


def __dir__():
    return (
        'cfg',
        'command',
        'forever',
        'init',
        'isop',
    )


Cfg = Default()
Cfg.debug   = False
Cfg.mod     = Cfg.mod or "cmd,err,thr,ver"
Cfg.name    = __file__.split(os.sep)[-2].lower()
Storage.wd  = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Storage.wd, f"{Cfg.name}.pid")
Cfg.start   = time.time()
Cfg.version = Cfg.version or "1"
Cfg.user    = getpass.getuser()


def command(txt, clt=None):
    cli = clt or CLI()
    evn = Message()
    evn.orig = object.__repr__(cli)
    evn.txt = txt
    parse(evn)
    cli.dispatch(evn)
    evn.wait()
    return evn


def forever():
    while 1:
        try:
            time.sleep(1.0)
        except:
            _thread.interrupt_main()


def isop(txt):
    for char in txt:
        if char in Cfg.opts:
            return True
    return False


def init(pkg, mnames, wait=False) -> []:
    res = []
    if not pkg:
        return res
    for mname in spl(mnames):
        module = getattr(pkg, mname, None)
        if not module:
            continue
        if "init" in dir(module):
            module._thr = launch(module.init)
            res.append(module)
    if wait:
        for mod in res:
            if "_thr" not in dir(mod):
                continue
            mod._thr.join()
    return res


def where():
    res = "/"
    for name in __file__.split(os.sep):
        res = os.path.join(res, name)
        if name == Cfg.name:
            break
    return res
