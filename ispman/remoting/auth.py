# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================
import logging
from twisted.internet.threads import deferToThread, defer
from pyamf.remoting.gateway import expose_request
from ispman.remoting import UnprotectedResource
from ispman.models.auth import AuthenticatedUser

import pyamf

ROLES = (ROLE_ADMIN, ROLE_RESELLER, ROLE_CLIENT, ROLE_DOMAIN) = range(1, 5)


log = logging.getLogger(__name__)

from ispman.decorators import utf8

class AuthenticationNeeded(Exception):
    """Exception which triggers the required authentication code on the
    flex side."""

class Authentication(UnprotectedResource):


    @expose_request
    def login(self, request, user):
        def failure(exception):
            raise AuthenticationNeeded
        d = deferToThread(self._login, request,
                          AuthenticatedUser(*user.values()))
        d.addErrback(failure)
        return d
#        return self._login(request, AuthenticatedUser(*user.values()))

    def _login(self, request, user):

        ldap = request.factory.ldap
        ldap_config = request.factory.ldap_config
        if user.login_type == ROLE_DOMAIN:
            base_bind_dn = 'ispmanDomain=%s,%%s' % ldap_config['base_dn']
            bind_dn = base_bind_dn % username
        elif user.login_type in (ROLE_CLIENT, ROLE_RESELLER):
            base_dn = "ou=ispman,%s" % ldap_config['base_dn']
            filter_base = "&(objectClass=%%s)(uid=%s)" % user.username
            log.debug('Base DN: %s', base_dn)
            if user.login_type == ROLE_CLIENT:
                scope  = "sub"
                ldap_filter = filter_base % "ispmanClient"
            elif user.login_type == ROLE_RESELLER:
                scope  = "one"
                ldap_filter = filter_base % "ispmanReseller"

            # search for bind_dn
            log.debug('SCOPE: %r, FILTER: %s', scope, ldap_filter)
            msg = ldap.search(base=base_dn, scope=scope, filter=ldap_filter,
                              attrs=[])
            entry = msg.entry(0)
            if not entry:
                log.debug('Entry not found for base: %r, scope: %r, filter: %r',
                          base_dn, scope, ldap_filter)
                raise AuthenticationNeeded
            log.debug("entry returned: %s", entry)
            bind_dn = entry.dn()
        elif user.login_type == ROLE_ADMIN:
            bind_dn = "uid=%s,ou=admins,%s" % (user.username,
                                               ldap_config['base_dn'])
        # Authenticate
        result =  ldap.bind(bind_dn, password=user.password)
        if result.code():
            log.debug('Failed to login')
            ldap.unbind()
            ldap.disconnect()
            raise AuthenticationNeeded

        log.debug('login OK for user "%s"', user.username)
        request.session.authenticated = True
        ldap.unbind()
        ldap.disconnect()
        return 'Logged In.'

    @expose_request
    def logout(self, request):
        request.session.expire()
        return 'Logged Out'

    @expose_request
    def overview(self, request):
        pass

