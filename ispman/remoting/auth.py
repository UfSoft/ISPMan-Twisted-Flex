# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from pyamf.remoting.gateway import expose_request
from ispman.remoting import UnprotectedResource

class AuthenticationNeeded(Exception):
    """Exception which triggers the required authentication code on the
    flex side."""

class Authentication(UnprotectedResource):

    @expose_request
    def login(self, request, username, password, login_type):
        print '\nREAL AUTH', request.session.__dict__
        if username == password:
            if not request.session:
                request.getSession()
            request.session.authenticated = True
            print '\nREAL AUTH', request.session.__dict__
            return 'Logged In.'
        raise AuthenticationNeeded

    @expose_request
    def logout(self, request):
        request.session.expire()
        return 'Logged Out'

