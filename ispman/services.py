# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from ispman.remoting import auth, domains, hosts, processes, timer

services = {
    'ISPManService.auth':       auth.Authentication(),
    'ISPManService.timer':      timer.Timer(),
    'ISPManService.domains':    domains.DomainsResource(),
    'ISPManService.hosts':      hosts.HostsResource(),
    'ISPManService.processes':  processes.ProcessesResource(),
}
