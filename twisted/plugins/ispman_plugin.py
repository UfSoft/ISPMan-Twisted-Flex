# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

try:
    from ispman.usage import ISPManService
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.getcwd(), 'python'))
    from ispman.usage import ISPManService

serviceMaker = ISPManService()
