# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from pyamf.flex import ArrayCollection
from ispman.remoting import *

log = logging.getLogger(__name__)

class HostsResource(Resource):

    @expose_request
    def get_hosts(self, request):
        def _get_hosts():
            hosts = ArrayCollection()
            for dn, data in dict(request.session.ispman.getHosts()).iteritems():
                host = {'dn': dn}
                for key, value in dict(data).iteritems():
                    host[key] = key=='ispmanHostAlias' and list(value) or value
                hosts.addItem(host)
            return hosts
        return defer.maybeDeferred(_get_hosts)
