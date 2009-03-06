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

class ProcessesResource(Resource):

    @expose_request
    def count(self, request):
        def get_current_count():
            return request.session.ispman.countProcessesInSession(
                request.session.uid
            )
        return defer.maybeDeferred(get_current_count)

    @expose_request
    def get_processes(self, request):
        def get_existing_processes():
            processes = ArrayCollection()
            existing_processes = request.session.ispman.getProcesses()
            if not existing_processes:
                return processes
            for k, v in dict(existing_processes).iteritems():
                process = {'dn': k}
                for key, value in dict(v).iteritems():
                    process[key] = value
                processes.addItem(process)
            return processes
#        from pprint import pprint
#        pprint(get_existing_processes())
        return defer.maybeDeferred(get_existing_processes)
