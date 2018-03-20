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


class UpdateSubnet(base.Scenario):
    """Update an OpenStack Subnet"""

    __scenario_type__ = "UpdateSubnet"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.subnet_id = self.options.get("subnet_id", None)

        self.openstack = self.options.get("openstack_paras", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        if not self.subnet_id:
            raise RuntimeError("Update subnet failed")

        openstack_paras = {'subnet': self.openstack}

        print (openstack_paras)
        res = op_utils.update_neutron_subnet(self.subnet_id, openstack_paras)

        if res:
            result.update({"subnet_create": 1})
            LOG.info("Update subnet successful!")
        else:
            result.update({"subnet_create": 0})
            LOG.error("Update subnet failed!")
            raise RuntimeError("Update subnet fail.")

