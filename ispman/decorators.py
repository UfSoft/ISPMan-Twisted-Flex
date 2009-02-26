# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from decorator import decorator

def utf8(func, *args, **kwargs):
    """Simple docorator which will encode every unicode arg or kwarg value to
    UTF-8 since python can't comunicate with perl using unicode.
    """
    _args = []
    for arg in args:
        if isinstance(arg, unicode):
            _args.append(arg.encode('utf-8'))
        else:
            _args.append(arg)
    args = tuple(_args)
    for key, value in kwargs.iteritems():
        if isinstance(value, unicode):
            kwargs[key] = value.encode('utf-8')
    return func(*args, **kwargs)
utf8 = decorator(utf8)
