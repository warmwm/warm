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


class SecGroupAddRule(base.Scenario):
    """Create an OpenStack flavor"""

    __scenario_type__ = "sec_group_add"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.sg_name = self.options.get("sg_name", "default")
        self.direction = self.options.get("direction", "ingress")
        self.protocol = self.options.get("protocol", "tcp")
        self.port_min = self.options.get("port_range_min", "22")
        self.port_max = self.options.get("port_range_max", "22")

        self.neutron_client = op_utils.get_neutron_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        sg_id = op_utils.get_security_group_id(self.neutron_client,
                                               sg_name=self.sg_name)
        status = op_utils.create_secgroup_rule(self.neutron_client,
                                               sg_id=sg_id,
                                               direction=self.direction,
                                               protocol=self.protocol,
                                               port_range_min=self.port_min,
                                               port_range_max=self.port_max)

        if status:
            result.update({"sg_create": 1})
            LOG.info("Add security group successful!")
        else:
            result.update({"sg_create": 0})
            LOG.error("Add security group failed!")
