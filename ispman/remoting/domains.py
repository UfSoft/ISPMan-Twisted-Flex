# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from ispman.remoting import *
log = logging.getLogger(__name__)

class DomainsResource(Resource):

    @expose_request
    def get_domains(self, request):
        domains = []

        for dn, data in dict(request.session.ispman.getDomains()).iteritems():
            domain = dict(data)
            domain['dn'] = dn
            domain['label'] = "%(ispmanDomain)s (%(ispmanDomainType)s)" % domain
            domains.append(domain)

        return domains
