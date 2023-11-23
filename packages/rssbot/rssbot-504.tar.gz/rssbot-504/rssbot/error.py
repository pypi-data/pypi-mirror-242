# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E1102


"errors"


import io
import traceback


from .censor import Censor
from .object import Object


def __dir__():
    return (
        'Errors',
    )


__all__ = __dir__()


class Errors(Object):

    errors = []
    shown  = []

    @staticmethod
    def add(exc) -> None:
        excp = exc.with_traceback(exc.__traceback__)
        Errors.errors.append(excp)

    @staticmethod
    def format(exc) -> str:
        res = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            res += line + "\n"
        return res

    @staticmethod
    def handle(exc) -> None:
        if Censor.output:
            txt = str(Errors.format(exc))
            if txt not in Errors.shown:
                Censor.output(txt)
                Errors.shown.append(txt)

    @staticmethod
    def show() -> None:
        for exc in Errors.errors:
            Errors.handle(exc)
