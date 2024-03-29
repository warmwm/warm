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


class DelRouterGateway(base.Scenario):
    """Unset an OpenStack router gateway"""

    __scenario_type__ = "DelRouterGateway"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.router_id = self.options.get("router_id", None)

        self.neutron_client = op_utils.get_neutron_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        status = op_utils.remove_gateway_router(self.neutron_client,
                                                router_id=self.router_id)
        if status:
            result.update({"del_router_gateway": 1})
            LOG.info("Delete router gateway successful!")
        else:
            result.update({"del_router_gateway": 0})
            LOG.error("Delete router gateway failed!")
