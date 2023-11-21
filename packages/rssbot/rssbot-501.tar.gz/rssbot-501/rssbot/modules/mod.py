# This file is placed in the Public Domain.
#
# pylint: disable=C0103,C0116,E0402,W0105


"available modules"


import os


def mod(event):
    path = os.path.join(os.sep, *__file__.split(os.sep)[:-1])
    modlist = [
               x[:-3] for x in os.listdir(path)
               if x.endswith(".py")
               and x not in ["__main__.py", "__init__.py"]
              ]
    event.reply(",".join(sorted(modlist)))
