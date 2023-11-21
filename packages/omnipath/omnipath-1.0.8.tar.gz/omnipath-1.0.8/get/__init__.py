#!/usr/bin/env python

import types
import wrapt


@wrapt.decorator
def pt(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)


def foo(cls, a = 2):

    return a + 1


class C:

    @classmethod
    def bar(cls, a = 1, b = 2):
        return 'hello bar'

C.foo = types.MethodType(pt(foo), C)
