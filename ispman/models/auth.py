# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

class AuthenticatedUser(object):

    def __init__(self, *args, **kwargs):
        if args and kwargs:
            raise TypeError("Don't pass both arguments and keyword arguments")
        if args and isinstance(args[0], dict):
            data = args[0]
        else:
            data = kwargs
        self.username = data.get('username').encode('utf-8')
        self.password = data.get('password').encode('utf-8')
        self.login_type = data.get('loginType')
        self.locale = data.get('locale', 'en_US')

    def __repr__(self):
        # Late import
        from ispman.remoting.auth import ROLES_MAP
        return "<%s %s(%s) - %s>" % (self.__class__.__name__,
                                     self.username, ROLES_MAP[self.login_type],
                                     self.locale)
