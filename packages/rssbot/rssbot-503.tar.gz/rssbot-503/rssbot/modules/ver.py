# This file is placed in the Public Domain.
#
# pylint:: disable=C,R


"version"


from .. import Cfg, Commands


def ver(event):
    event.reply(f"{Cfg.name.upper()} {Cfg.version}")


Commands.add(ver)
