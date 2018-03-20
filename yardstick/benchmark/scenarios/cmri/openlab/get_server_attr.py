# ############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
# ############################################################################

from __future__ import print_function
from __future__ import absolute_import

import logging

from yardstick.benchmark.scenarios import base

LOG = logging.getLogger(__name__)


class GetServerAttr(base.Scenario):
    """
    Execute a cold migration for two hosts

    """

    __scenario_type__ = "GetServerAttr"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.options = self.scenario_cfg.get('options', {})

    def run(self, result):

        server = self.options.get('server', {})

        keys = self.scenario_cfg.get('output', '').split()
        values = [server.get(key, '') for key in keys]
        return self._push_to_outputs(keys, values)
