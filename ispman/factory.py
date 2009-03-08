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

import pyamf
from pyamf import amf3
from pyamf.remoting.gateway import expose_request
from pyamf.remoting.gateway.twisted import TwistedGateway

from ispman.services import services
from ispman.remoting.auth import AuthenticationNeeded
# ISPMan Models
from ispman.models.auth import AuthenticatedUser

import logging
import perl

ISPMAN_AS_NAMESPACE = 'org.ufsoft.ispman'

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


    def setup_pyamf(self):
        # Setup PyAMF
        # Set this to true so that returned objects and arrays are bindable
        MODELS_NAMESPACE = "%s.models" % ISPMAN_AS_NAMESPACE
        amf3.use_proxies_default = True
        #
        pyamf.register_class(
            AuthenticatedUser, "%s.AuthenticatedUser" % MODELS_NAMESPACE)

    def build_resources(self, config):
        resource = Resource()

        # Add the config/static files we're supplying
        static_files_dir = join(dirname(__file__), 'static')
        for filename in listdir(static_files_dir):
            filepath = join(static_files_dir, filename)
            if filename == 'index.html':
                filename = ''
            resource.putChild(filename, File(filepath))

        # Override with the files the user provide from it's dir
        if isdir(config.static_files):
            static_files_dir = config.static_files
            for filename in listdir(static_files_dir):
                filepath = join(static_files_dir, filename)
                if filename == 'index.html':
                    # Serve index.html from /
                    filename = ''
                resource.putChild(filename, File(filepath))

        gateway = TwistedGateway(services, expose_request=False,
                                 preprocessor=self.preprocessor)
        gateway.logger = logging.getLogger('ispman.pyamf')
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
            ispman_perl = self.get_ispman()
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

        log.debug('ISPMan(perl) Is Now Setup')

    def get_ispman(self):
        ispman = perl.eval('$ENV{"HTTP_USER_AGENT"} = "FLEX-CP"; '
                           '$ispman = ISPMan->new() or die "$@"')
#        print dict(ispman.getUsers('demo.ufsoft.org'))
        from ispman.models.user import DomainUser
        for dn, details_hash in dict(ispman.getUsers('demo1.ufsoft.org',
              ('uid', 'dn', 'givenName', 'sn', 'cn', 'ispmanCreateTimestamp',
              'ispmanUserId', 'mailLocalAddress', 'userPassword',
              'mailForwardingAddress', 'mailQuota', 'mailAlias',
              'FTPQuotaMBytes', 'FTPStatus'))).iteritems():
            print dict(details_hash)
#            for k, v in dict(details_hash).iteritems():
#                if k=='uid':
#                    print k, list(v)
#                else:
#                    print k, v
            i = DomainUser(dn, details_hash)
            print 1, i
            for k, v in  i.__dict__.iteritems():
                print k, v
        return ispman

    def get_ldap(self):
        if not self._ldap:
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
        print '\n\n\n Preprocess', args, kwargs
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


