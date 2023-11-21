# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0212,W0105,W0613,W0406,W0611,E0102


"main"


import readline
import sys
import time


from .censors import Censor
from .command import Commands
from .excepts import Errors
from .message import Message
from .parsers import parse
from .reactor import CLI
from .runtime import cfg, command, forever, isop, scan
from .utility import daemon, lsmod, privileges, wrap


from . import modules


class CLI(CLI):

    def say(self, channel, txt):
        txt = txt.encode('utf-8', 'replace').decode()
        sys.stdout.write(txt)
        sys.stdout.write("\n")
        sys.stdout.flush()


class Console(CLI):

    def poll(self) -> Message:
        evt = Message()
        evt.orig = object.__repr__(self)
        evt.txt = input("> ")
        evt.type = "command"
        return evt


def main():
    parse(cfg, " ".join(sys.argv[1:]))
    if isop("v"):
        Censor.output = print
        dte = time.ctime(time.time()).replace("  ", " ")
        print(f"{cfg.name.upper()} started {cfg.opts.upper()} started {dte}")
    wait = False
    if isop("d"):
        daemon(cfg.pidfile, isop("v"))
        privileges(cfg.user)
        wait = True
    if isop("cd"):
        scan(modules, cfg.mod, not isop("x"), isop("w"))
    if isop("c"):
        csl = Console()
        if isop("t"):
            csl.threaded = True
        csl.start()
        wait = True
    if wait:
        forever()
        return
    scan(modules, cfg.mod)
    cli = CLI()
    command(cfg.otxt, cli)


def wrapped():
    wrap(main)
    Errors.show()


if __name__ == "__main__":
    wrapped()
        