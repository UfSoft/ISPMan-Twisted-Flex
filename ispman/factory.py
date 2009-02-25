# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================


from os import listdir
from os.path import dirname, join, isfile, isdir

from OpenSSL import SSL

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.static import File

from pyamf.remoting.gateway import expose_request
from pyamf.remoting.gateway.twisted import TwistedGateway

from ispman.services import services
from ispman.remoting.auth import AuthenticationNeeded

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)

class ISPManFactory(Site):
    def __init__(self, config, logPath=None, timeout=60*60*12):
        resource = Resource()
        # Add any xml config files to our resources
        if isdir(config.static_files):
            static_files_dir = config.static_files
            for filename in listdir(static_files_dir):
                filepath = join(static_files_dir, filename)
                if filename == 'index.html':
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
        gateway.logger = logging.getLogger('ispman.pyamf')

        resource.putChild('service', gateway)
#        resource.putChild('', File('/home/vampas/projects/ISPMan/flex/deploy/ispman.swf'))
        Site.__init__(self, resource, logPath, timeout)
        self.config = config

    @expose_request
    def preprocessor(self, request, service_request, *args, **kwargs):
        if not request.session:
            request.getSession()
        if service_request.method == 'login':
            return
        try:
            return request.session.authenticated
        except AttributeError:
            raise AuthenticationNeeded

    def getContext(self):
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_certificate_file(self.config.certificate_file)
        ctx.use_privatekey_file(self.config.privatekey_file)
        return ctx


