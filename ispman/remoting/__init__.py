# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from twisted.web.resource import Resource as BaseResource

class Resource(BaseResource):
    """Protected resource, requests must be authenticated first in order to
    get access, else a 401 is raised."""

class UnprotectedResource(BaseResource):
    """Base class for unprotected resources"""


