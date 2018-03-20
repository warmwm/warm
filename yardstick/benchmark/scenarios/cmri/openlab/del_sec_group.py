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


class DelSecGroup(base.Scenario):
    """Delete an OpenStack security group"""

    __scenario_type__ = "DelSecGroup"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.secgroup_id = self.options.get("secgroup_id", None)

        self.neutron_client = op_utils.get_neutron_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        status = op_utils.delete_security_group(self.neutron_client,
                                                secgroup_id=self.secgroup_id)
        if status:
            result.update({"del_sec_group": 1})
            LOG.info("Delete security group successful!")
        else:
            result.update({"del_sec_group": 0})
            LOG.error("Delete security group failed!")
