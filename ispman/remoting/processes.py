# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from ispman.remoting import *

log = logging.getLogger(__name__)

class ProcessesResource(Resource):

    @expose_request
    def count(self, request):
        def get_current_count():
            return request.session.ispman.countProcessesInSession(
                request.session.uid
            )
        return deferToThread(get_current_count)

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
        return deferToThread(get_existing_processes)

    @expose_request
    def delete_process(self, request, process):
        log.debug(process)
        def _delete_process():
            return request.session.ispman.deleteProcessByPID(
                int(process.get('ispmanPid'))
            )
        return deferToThread(_delete_process)

    @expose_request
    def update_process(self, request, process):
        log.debug(process)
        process = Hash(process)
        def _update_process():
            # Can't just call ispman.modifyProcess since that's meant for
            # the perl CP, we just do what the function does minus what we don't
            # need
            return request.session.ispman.updateEntryWithData(
                process.param('dn'), {
                    'ispmanStatus': process.param('ispmanStatus'),
                    'ispmanPid': process.param('ispmanPid'),
                    'ispmanHostName': process.param('ispmanHostName'),
                }
            )
        return deferToThread(_update_process)
