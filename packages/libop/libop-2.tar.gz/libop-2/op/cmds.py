# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718


"commands"


from .broker import Broker
from .error  import Errors
from .object import Object
from .parse  import parse


def __dir__():
    return (
        'Commands',
    )


__all__ = __dir__()


class Commands(Object):

    cmds = Object()

    def __init__(self):
        Object.__init__(self)
        Broker.add(self)

    @staticmethod
    def add(func) -> None:
        setattr(Commands.cmds, func.__name__, func)

    def announce(self, txt):
        pass

    @staticmethod
    def dispatch(evt) -> None:
        parse(evt)
        func = getattr(Commands.cmds, evt.cmd, None)
        if not func:
            evt.ready()
            return
        try:
            func(evt)
            evt.show()
        except Exception as exc:
            Errors.add(exc)
        evt.ready()
 
    def say(self, txt):
        raise NotImplementedError("Commands.say")
