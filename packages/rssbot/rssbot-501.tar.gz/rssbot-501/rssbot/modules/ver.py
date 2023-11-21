# This file is placed in the Public Domain.
#
#


"version"


from ..runtime import cfg


def ver(event):
    event.reply(f"{cfg.name.upper()} {cfg.version}")
