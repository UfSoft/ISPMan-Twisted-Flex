# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from ispman.remoting import *
from ispman.models.user import DomainUser
from pyamf.flex import ArrayCollection

log = logging.getLogger(__name__)

class DomainsResource(Resource):

    @expose_request
    def get_domains(self, request):
        domains = ArrayCollection()

        for dn, data in dict(request.session.ispman.getDomains()).iteritems():
            domain = dict(data)
            domain['dn'] = dn
            domain['label'] = "%(ispmanDomain)s (%(ispmanDomainType)s)" % domain
            print 333, domain
            domains.addItem(domain)

        return domains

    @expose_request
    def get_users(self, request, domain):
        attrs_list = ('dn', 'givenName', 'sn', 'cn', 'ispmanCreateTimestamp',
                      'ispmanUserId', 'mailLocalAddress', 'userPassword',
                      'mailForwardingAddress', 'mailQuota', 'mailAlias',
                      'FTPQuotaMBytes', 'FTPStatus')
        domain_users = request.session.ispman.getUsers(
            Hash(domain).get('ispmanDomain'), attrs_list)
        users = ArrayCollection()
        for dn, details_hash in dict(domain_users).iteritems():
            user = DomainUser(dn, details_hash)
            users.addItem(user)
