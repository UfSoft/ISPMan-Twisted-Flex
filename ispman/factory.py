# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================


from os import listdir
from os.path import dirname, join, isdir
import sys

from OpenSSL import SSL

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.static import File

from pyamf.remoting.gateway import expose_request
from pyamf.remoting.gateway.twisted import TwistedGateway

from ispman.services import services
from ispman.remoting.auth import AuthenticationNeeded

import logging
import perl

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)

log = logging.getLogger(__name__)

class ISPManFactory(Site):
    _ispman = _ldap = _ldap_config = None
    def __init__(self, config, logPath=None, timeout=60*60*12):
        resource = self.build_resources(config)
        Site.__init__(self, resource, logPath, timeout)
        self.config = config

    def build_resources(self, config):
        resource = Resource()
        # Add any xml config files to our resources
        if isdir(config.static_files):
            static_files_dir = config.static_files
            for filename in listdir(static_files_dir):
                filepath = join(static_files_dir, filename)
                if filename == 'index.html':
                    # Serve index.html from /
                    filename = ''
                resource.putChild(filename, File(filepath))

        # Add the config files we're supplying
        static_files_dir = join(dirname(__file__), 'static')
        for filename in listdir(static_files_dir):
            filepath = join(static_files_dir, filename)
            if filename == 'index.html':
                filename = ''
            resource.putChild(filename, File(filepath))

        gateway = TwistedGateway(services, expose_request=False,
                                 preprocessor=self.preprocessor)
        #gateway.logger = logging.getLogger('ispman.pyamf')
        resource.putChild('service', gateway)
        return resource

    def init_perl(self):
        ispman_libs = join(self.config.ispman_perl_install, 'lib')
        print "ISPMan Perl Libs Path", ispman_libs
        # Get Perl's @INC reference
        inc = perl.get_ref("@INC")
        # Add ISPMan lib directory to perl's @INC
        inc.append(ispman_libs)
        # Setup an ISPMan instance
        perl.require('ISPMan')
        perl.require('CGI')
        try:
            ispman_perl = perl.eval('$ENV{"HTTP_USER_AGENT"} = "ISPMAN-CCP"; ' +
                                    '$ispman = ISPMan->new() or die "$@"')
        except Exception, err:
            print "Failed to connect to the ISPMan Perl backend:", err
            sys.exit(1)

        self.ldap_config = dict(host    = ispman_perl.getConf('ldapHost'),
                                version = ispman_perl.getConf('ldapVersion'),
                                base_dn = ispman_perl.getConf('ldapBaseDN'))

        perl.require('Net::LDAP')
        log.debug('After require LDAP')
        eval_string = 'Net::LDAP->new( "%s",version => %s ) or die "$@";'
        log.debug('Eval String: %s', eval_string % (
                        self.ldap_config['host'], self.ldap_config['version']))
        try:
            ldap = perl.eval(eval_string % (self.ldap_config['host'],
                                            self.ldap_config['version']))
        except perl.PerlError, error:
            print "Failed to connect to LDAP Server: %s" % error
            sys.exit(1)

        log.debug('After LDAP setup')
        ldap.disconnect()
        log.debug('LDAP works, disconnecting...')

        self.ldap_config['allowed_user_attributes'] = (
            'dn', 'dialupAccess', 'radiusProfileDn', 'uid', 'uidNumber',
            'gidNumber', 'homeDirectory', 'loginShell', 'ispmanStatus',
            'ispmanCreateTimestamp', 'ispmanUserId', 'ispmanDomain',
            'DestinationAddress', 'DestinationPort', 'mailQuota', 'mailHost',
            'fileHost', 'cn', 'mailRoutingAddress', 'FTPStatus',
            'FTPQuotaMBytes', 'mailAlias', 'sn', 'mailLocalAddress',
            'userPassword', 'mailForwardingAddress', 'givenName')

        self.ldap_config['updatable_attributes'] = (
            'ispmanStatus', 'mailQuota', 'mailAlias', 'sn', 'userPassword',
            'givenName', 'updateUser', 'uid', 'mailForwardingAddress',
            'ispmanDomain', 'FTPQuotaMBytes', 'FTPStatus', 'mailHost',
            'fileHost', 'dialupAccess', 'radiusProfileDN')

        self.perl = ispman_perl
        log.debug('ISPMan(perl) Is Now Setup')

    def get_ispman(self):
        if not self._ispman:
            self._ispman = perl.eval('$ENV{"HTTP_USER_AGENT"} = "ISPMAN-CCP"; '+
                                     '$ispman = ISPMan->new() or die "$@"')
        return self._ispman

    ispman = property(get_ispman)

    def get_ldap(self):
        if not self._ldap:
            #perl.require('Net::LDAP')
            log.debug('Grabbing New LDAP Connection')
            eval_string = 'Net::LDAP->new( "%s",version => %s ) or die "$@";'
            log.debug('Eval String: %s', eval_string % (
                      self.ldap_config['host'], self.ldap_config['version']))
            try:
                self._ldap = perl.eval(eval_string % (
                    self.ldap_config['host'], self.ldap_config['version']))
            except perl.PerlError, error:
                print "Failed to connect to LDAP Server: %s" % error
                sys.exit(1)
            log.debug('New LDAP Connection retrieved')
        return self._ldap

    ldap = property(get_ldap)


    @expose_request
    def preprocessor(self, request, service_request, *args, **kwargs):
        try:
            if not request.session:
                request.getSession()
            request.factory = self
            if service_request.method == 'login':
                return
            try:
                return request.session.authenticated
            except AttributeError:
                raise AuthenticationNeeded
        except Exception, err:
            print 123456
            raise err

    def getContext(self):
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_certificate_file(self.config.certificate_file)
        ctx.use_privatekey_file(self.config.privatekey_file)
        return ctx


