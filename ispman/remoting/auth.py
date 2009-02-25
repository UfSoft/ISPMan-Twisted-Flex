# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================
import logging
from twisted.internet.threads import deferToThread
from pyamf.remoting.gateway import expose_request
from ispman.remoting import UnprotectedResource

ROLES = (ROLE_ADMIN, ROLE_RESELLER, ROLE_CLIENT, ROLE_DOMAIN) = range(1, 5)


log = logging.getLogger(__name__)

class AuthenticationNeeded(Exception):
    """Exception which triggers the required authentication code on the
    flex side."""

class Authentication(UnprotectedResource):

    @expose_request
    def login(self, request, username, password, login_type):
        print 12345, repr(username), repr(password), repr(login_type)
#        def failure(exception):
#            raise exception
#            print 12345, args
#            raise AuthenticationNeeded
#
#        deferred = deferToThread(self._login, request, username, password,
#                                               login_type)
#        deferred.addErrback(failure)
#        return deferred
        return self._login(request, username, password, login_type)

    def _login(self, request, username, password, login_type):
        ldap = request.ldap()
        if login_type == ROLE_DOMAIN:
            base_bind_dn = 'ispmanDomain=%s,%%s' % request.ldap_config['base_dn']
            bind_dn = base_bind_dn % username
        elif login_type in (ROLE_CLIENT, ROLE_RESELLER):
            base_dn = "ou=ispman,%s" % request.ldap_config['base_dn']
            log.debug('Base DN: %s', base_dn)
            if login_type == ROLE_CLIENT:
                scope  = "sub"
                ldap_filter = "&(objectClass=ispmanClient)(uid=%s)" % username
            elif login_type == ROLE_RESELLER:
                scope  = "one"
                ldap_filter = "&(objectClass=ispmanReseller)(uid=%s)" % username
            # search for bind_dn
            log.debug('SCOPE: %r, FILTER: %s', scope, ldap_filter)
            msg = ldap.search(base=base_dn, scope=scope, filter=str(ldap_filter), attrs=[])
            entry = msg.entry(0)
            if not entry:
                log.debug('Entry not found for base: %r, scope: %r, filter: %r',
                          base_dn, scope, ldap_filter)
                raise AuthenticationNeeded
            log.debug("entry returned: %s", entry)
            bind_dn = entry.dn()
        elif login_type == ROLE_ADMIN:
            bind_dn = "uid=%s,ou=admins,%s" % (username,
                                               request.ldap_config['base_dn'])
        # Authenticate
        class BindInfo(object):
            __slots__ = ('dn',)
            def __init__(self, bind_dn):
                self.dn = bind_dn

            def __eq__(self, newobj):
                self.db == newobj.dn

            def __ne__(self, newobj):
                self.db != newobj.dn

        log.debug('Binding to LDAP with the DN: "%s"', bind_dn)
        print ldap.bind
        result = ldap.bind()
        print result, result.code()
        #result =  ldap.bind(BindInfo(bind_dn), password=password)
        result =  ldap.bind(bind_dn, password=password)
        if result.code():
            log.debug('Failed to login')
            print result.error()
            ldap.unbind()
            raise AuthenticationNeeded

        log.debug('login OK for user "%s"', username)
        request.session.authenticated = True
        return 'Logged In.'

    @expose_request
    def logout(self, request):
        request.session.expire()
        return 'Logged Out'

