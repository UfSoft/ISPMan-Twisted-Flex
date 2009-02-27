# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

class AuthenticatedUser(object):
    def __init__(self, username=None, password=None, loginType=None):
        self.username = username.encode('utf-8')
        self.password = password.encode('utf-8')
        self.login_type = loginType
