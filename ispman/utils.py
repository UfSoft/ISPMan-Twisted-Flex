# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

class Hash(dict):
    def get(self, key):
        value = dict.get(self, key)
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        return value
    param = get

    def getlist(self, key):
        values = self.get(key)
        if isinstance(values, basestring):
            return [values]
        elif not values:
            return []
        values = list(values)
        for idx, value in enumerate(values):
            if isinstance(value, unicode):
                values[idx] = value.encode('utf-8')
        return values

    def getint(self, key):
        return int(self.get(key))
