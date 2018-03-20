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

from yardstick.benchmark.scenarios import base
import yardstick.common.openstack_utils as op_utils

LOG = logging.getLogger(__name__)


class GetNetworkID(base.Scenario):
    """Get a network ID by name"""

    __scenario_type__ = "GetNetworkID"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg.get("options", {})

        self.network_name = self.options.get("network_name")

        self.neutron_client = op_utils.get_neutron_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        id = op_utils.get_network_id(self.neutron_client, self.network_name)

        keys = self.scenario_cfg.get('output', '').split()

        if id:
            LOG.info("Get network ID successful!")
            values = [0, id]
        else:
            LOG.info("Get network ID failed!")
            values = [1]

        return self._push_to_outputs(keys, values)

