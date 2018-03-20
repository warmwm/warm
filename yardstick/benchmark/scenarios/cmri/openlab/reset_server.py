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
import subprocess

from yardstick.benchmark.scenarios import base
from yardstick.common import constants as consts
import yardstick.common.openstack_utils as op_utils

LOG = logging.getLogger(__name__)


class ResetServer(base.Scenario):
    """Reset the state of a server"""

    __scenario_type__ = "ResetServer"


    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.server_id = self.options.get("server_id", None)
        self.state = self.options.get("state", "error")

        self.nova_client = op_utils.get_nova_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        try:
            op_utils.reset_server_state(self.server_id, self.state)
            LOG.info("Reset server state successful!")
        except Exception:
            LOG.info("Reset server state failed!")
