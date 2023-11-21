# This file is placed in the Public Domain.
#
#


"runtime"


import getpass
import os
import time
import _thread


from .command import Commands
from .message import Message
from .objects import Default
from .parsers import parse
from .reactor import CLI
from .storage import Storage
from .threads import launch
from .utility import spl


def __dir__():
    return (
        'cfg',
        'command',
        'forever',
        'isop',
        'scan'
    )


cfg = Default()
cfg.mod     = cfg.mods or "cmd,irc,rss,ver"
cfg.name    = cfg.name or "rssbot"
Storage.wd  = os.path.expanduser(f"~/.{cfg.name}")
cfg.pidfile = os.path.join(Storage.wd, f"{cfg.name}.pid")
cfg.version = cfg.version or "501"
cfg.user    = getpass.getuser()


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
        if char in cfg.opts:
            return True
    return False


def scan(pkg, mnames, init=False, wait=False) -> []:
    res = []
    if not pkg:
        return res
    for mname in spl(mnames):
        module = getattr(pkg, mname, None)
        if not module:
            continue
        Commands.scan(module)
        Storage.scan(module)
        res.append(module)
        if init and "init" in dir(module):
            module._thr = launch(module.init)
    if wait:
        for mod in res:
            if "_thr" not in dir(mod):
                continue
            mod._thr.join()
    return res
