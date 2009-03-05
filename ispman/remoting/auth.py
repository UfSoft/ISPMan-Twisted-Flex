# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from ispman.remoting import *
from ispman.models.auth import AuthenticatedUser

ROLES = (ROLE_ADMIN, ROLE_RESELLER, ROLE_CLIENT, ROLE_DOMAIN) = range(1, 5)
ROLES_MAP = {
    ROLE_ADMIN: 'admin',
    ROLE_RESELLER: 'reseller',
    ROLE_CLIENT: 'client',
    ROLE_DOMAIN: 'domain'
}
log = logging.getLogger(__name__)

class AuthenticationNeeded(Exception):
    """Exception which triggers the required authentication code on the
    flex side."""


class ISPManSession(dict):
    """This class is responsible for mimic'ing Perl's CGI sessions in order to
    allow ISPMan to do it's filtering. For example, which domains does the user
    have access to, etc..."""

    def param(self, name):
        return self.get(name)


class Authentication(Resource):

    @expose_request
    def login(self, request, user):
        def failure(exception):
            print exception
            raise AuthenticationNeeded
        d = deferToThread(self._login, request,
                          AuthenticatedUser(*user.values()))
        d.addErrback(failure)
        return d

    def _login(self, request, user):
        if getattr(request.session, 'authenticated', False):
            return 'Logged In.'
        ldap = request.factory.ldap
        ldap_config = request.factory.ldap_config
        ispman_session = ISPManSession()
        if user.login_type == ROLE_DOMAIN:
            base_bind_dn = 'ispmanDomain=%s,%%s' % ldap_config['base_dn']
            bind_dn = base_bind_dn % user.username
            ispman_session['ispmanDomain'] = user.username
        elif user.login_type in (ROLE_CLIENT, ROLE_RESELLER):
            base_dn = "ou=ispman,%s" % ldap_config['base_dn']
            filter_base = "&(objectClass=%%s)(uid=%s)" % user.username
            log.debug('Base DN: %s', base_dn)
            if user.login_type == ROLE_CLIENT:
                scope  = "sub"
                ldap_filter = filter_base % "ispmanClient"
                search_attr = 'ispmanClientId'
            elif user.login_type == ROLE_RESELLER:
                scope  = "one"
                ldap_filter = filter_base % "ispmanReseller"
                search_attr = 'ispmanResellerId'

            # search for bind_dn
            log.debug('SCOPE: %r, FILTER: %s', scope, ldap_filter)
            msg = ldap.search(base=base_dn, scope=scope, filter=ldap_filter,
                              attrs=[search_attr])
            entry = msg.entry(0)
            if not entry:
                log.debug('Entry not found for base: %r, scope: %r, filter: %r',
                          base_dn, scope, ldap_filter)
                raise AuthenticationNeeded
            log.debug("entry returned: %s", entry)
            bind_dn = entry.dn()
            ispman_session[search_attr] = entry.get_value(search_attr)
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

        user.bind_dn = bind_dn
        request.session.user = user
        request.session.authenticated = True

        # Do the necessary tweaks to make ISPMan not drop it's security models
        ispman = request.factory.get_ispman()
        ispman.remote_user(request.session.user.username)
        ispman['sessID'] = request.session.uid
        ispman_session.update({
            'uid': user.username,
            'logintype': ROLES_MAP[user.login_type],
            'language': user.language,
        })
        ispman['session'] = ispman_session
        request.session.ispman = ispman

        ldap.unbind()
        ldap.disconnect()
        log.debug('login OK for user "%s"', user.username)
        return 'Logged In.'

    @expose_request
    def logout(self, request):
        def _logout():
            request.session.expire()
            return 'Logged Out'
        return defer.maybeDeferred(_logout)

    @expose_request
    def overview(self, request):
        ispman = request.session.ispman
        func = None
        def get_admin_level_data():
            data = [
                {'label': 'AdminID:', 'data': request.session.user.username },
                {'label': 'Number of Domains Hosted:',
                 'data': ispman.getDomainsCount()},
                {'label': 'Number of Websites:',
                 'data': ispman.getVhostsCount()},
                {'label': 'Number of User Accounts:',
                 'data': ispman.getUsersCount()},
                {'label': 'Number of Databases:',
                 'data': ispman.getAllDatabaseCount()}
            ]
            return data

        def get_reseller_level_data():
            data = [
                {'label': 'ResselerID:', 'data': request.session.user.username },
            ]
            return data

        def get_client_level_data():
            data = [
                {'label': 'ClientID:', 'data': request.session.user.username },
            ]
            return data

        if request.session.user.login_type == ROLE_ADMIN:
            func = get_admin_level_data
        elif request.session.user.login_type == ROLE_RESELLER:
            func = get_reseller_level_data
        elif request.session.user.login_type == ROLE_CLIENT:
            func = get_client_level_data

        def failure(exception):
            print '\n\n\n123\n\n\n', exception

        d = deferToThread(func)
        d.addErrback(failure)
        return d

