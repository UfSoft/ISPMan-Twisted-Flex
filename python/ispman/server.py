# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

import os
from pyamf import amf3
from pyamf.remoting.gateway import expose_request
from pyamf.remoting.gateway.twisted import TwistedGateway
from twisted.application import service, strports
from twisted.web import resource, server, static


from ispman.services import services
from ispman.remoting.auth import AuthenticationNeeded

@expose_request
def preprocessor(request, service_request, *args, **kwargs):
    if not request.session:
        request.getSession()
    if service_request.method == 'login':
        return
    try:
        return request.session.authenticated
    except AttributeError:
        raise AuthenticationNeeded


print "Exposed Services", services
gateway = TwistedGateway(services, expose_request=False,
                         preprocessor=preprocessor)
#from twisted.python import log
#log.error = log.err

import logging

handler = logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)

gateway.logger = logging.getLogger('ispman.pyamf')


print logging._handlers
print logging._handlerList

# A base root resource for the twisted.web server
root = resource.Resource()

static_files_dir = os.path.join(os.path.dirname(__file__), 'static')
for filename in os.listdir(static_files_dir):
    filepath = os.path.join(static_files_dir, filename)
    root.putChild(filename, static.File(filepath))

root.putChild('service', gateway)


print 'Running AMF gateway on http://localhost:8080'

application = service.Application('PyAMF Sample Remoting Server')
server = strports.service('tcp:8080', server.Site(root))
server.setServiceParent(application)


