# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================
import sys
from types import ModuleType
from twisted.plugin import IPlugin
from twisted.application import internet, service
from twisted.application.service import IServiceMaker
from twisted.internet import reactor, defer
from twisted.python import usage
from ConfigParser import SafeConfigParser

from babel.core import Locale
from os import makedirs, listdir
from os.path import abspath, dirname, basename, expanduser, isdir, isfile, join
from sys import argv
from ispman import __version__
from ispman.factory import ISPManFactory
from zope.interface import implements

sys.modules['ispman.config'] = config = ModuleType('config')

class ISPManOptions(usage.Options):

    optParameters = [
        ['config', 'c', None, "Configuration Directory"],
    ]

    def opt_version(self):
        """Show Version"""
        print basename(argv[0]), '-', __version__
    opt_v = opt_version

    def opt_help(self):
        """Show this help message"""
        super(usage.Options, self).opt_help()
    opt_h = opt_help

    def postOptions(self):
        self.opts.config = abspath(expanduser(self.opts.get('config')))

    def getService(self, options):
        if not isdir(options.config):
            makedirs(options.config)
        parser = SafeConfigParser()

        config_file = join(options.config, 'ispman.cfg')
        if not isfile(config_file):
            parser.add_section('ispman')
            parser.set('ispman', 'ispman_perl_install', '')
            parser.set('ispman', 'static_files', '%(here)s/static_files')
            parser.set('ispman', 'server_port', '8080')
            parser.set('ispman', 'privatekey_file', '%(here)/service.key')
            parser.set('ispman', 'certificate_file', '%(here)/service.cert')
            parser.write(open(config_file, 'w'))
        else:
            parser.readfp(open(config_file))
        parser.set('ispman', 'here', options.config)

        config.ispman_perl_install = abspath(parser.get('ispman',
                                                        'ispman_perl_install'))
        config.static_files = parser.get('ispman', 'static_files')
        config.server_port = parser.getint('ispman', 'server_port')
        config.privatekey_file = parser.get('ispman', 'privatekey_file')
        config.certificate_file = parser.get('ispman', 'certificate_file')

        config.locales = {}
        locales_path = join(dirname(__file__), 'locale')
        for locale in listdir(locales_path):
            locale_file = join(locales_path, locale, 'LC_MESSAGES',
                               'messages.mo')
            if isfile(locale_file):
                config.locales[locale] = {
                    'path': locale_file,
                    'name': Locale.parse(locale).display_name
                }

        return ISPManFactory(config)

class ISPManService(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'ispman'
    description = 'ISPMan Control Panel Service'
    options = ISPManOptions

    def makeService(self, options):
        application = service.Application("ISPMan Control Panel") #, uid, gid)
        services = service.IServiceCollection(application)

        factory = options.getService(options)

        factory.init_perl()
        internet.SSLServer(
            config.server_port, factory, factory).setServiceParent(services)#
        return services


