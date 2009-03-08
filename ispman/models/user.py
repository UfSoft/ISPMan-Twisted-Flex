# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from ispman.utils import Hash

class DomainUser(object):
    def __init__(self, dn, details_hash):
        self.dn = dn
        details_hash = Hash(details_hash)
        self.uid = list(details_hash.get('uid'))
        self.givenName = details_hash.get('givenName')
        self.sn = details_hash.get('sn') # surname
        self.cn = details_hash.get('cn') # givenName + surname
        self.ispmanUserId = details_hash.get('ispmanUserId')
        self.mailLocalAddress = details_hash.get('mailLocalAddress')
        self.userPassword = details_hash.get('userPassword')
        self.mailForwardingAddress = details_hash.getlist('mailForwardingAddress')
        self.FTPStatus = details_hash.get('FTPStatus')
        self.FTPQuotaMBytes = details_hash.getint('FTPQuotaMBytes')
        self.ispmanCreateTimestamp = details_hash.getint('ispmanCreateTimestamp')
        self.mailAlias = details_hash.getlist('mailAlias')

    def __repr__(self):
        return "<%s - UID: %s; CN: '%s';>" % (self.__class__.__name__,
                                              self.uid, self.cn)
