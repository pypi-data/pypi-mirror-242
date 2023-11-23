# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,W0702


"runtime"


import getpass
import os
import time
import _thread


from .event  import Event
from .object import Default
from .parse  import parse
from .react  import CLI
from .disk   import Storage
from .thread import launch
from .util   import spl


def __dir__():
    return (
        'cfg',
        'command',
        'forever',
        'init',
        'isop',
    )


Cfg = Default()


def command(txt, clt=None):
    cli = clt or CLI()
    evn = Event()
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
