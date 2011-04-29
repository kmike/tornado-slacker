"""
Slacker's adisp library wrapper.

Removes the need to call 'adisp.async(proceed)' manually on yield for Slacker
and Postponed objects: they can now be yielded directly.
"""

from slacker.adisp._adisp import CallbackDispatcher, async
from slacker.postpone import Postponed, Slacker


class _SlackerCallbackDispatcher(CallbackDispatcher):
    def call(self, callers):
        if isinstance(callers, (Postponed, Slacker)):
            callers = async(callers.proceed)()
        return super(_SlackerCallbackDispatcher, self).call(callers)


def process(func):
    def wrapper(*args, **kwargs):
        _SlackerCallbackDispatcher(func(*args, **kwargs))
    return wrapper
