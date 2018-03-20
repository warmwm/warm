##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from __future__ import print_function
from __future__ import absolute_import

import logging
import ping

from yardstick.benchmark.scenarios import base

LOG = logging.getLogger(__name__)

TIMEOUT = 0.05
PACKAGE_SIZE = 64
REPEAT_TIMES = 3000


class PingServer(base.Scenario):
    """Get a server by name"""

    __scenario_type__ = "PingServer"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg.get('options', {})

    def run(self, result):
        server_ip = self.options.get('server_ip', '')

        connected = 1
        for i in range(REPEAT_TIMES):
            res = ping.do_one(server_ip, TIMEOUT, PACKAGE_SIZE)
            if res:
                connected = 0
                break

        keys = self.scenario_cfg.get('output', '').split()
        values = [connected]
        return self._push_to_outputs(keys, values)
