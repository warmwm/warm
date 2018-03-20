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


class UpdateFlavorName(base.Scenario):
    """Update an OpenStack flavor name"""

    __scenario_type__ = "UpdateFlavorName"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']
        self.vcpus = self.options.get("vcpus","2")
        self.ram = self.options.get("ram","2048")
        self.disk = self.options.get("disk","5")
        self.flavor_name_new = self.options.get("flavor_name_new","flavor_name_new01")
        self.flavor_name = self.options.get("flavor_name", "TestFlavor")
        
        self.nova_client = op_utils.get_nova_client()
        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

    #   LOG.info("Update flavor name : %s", self.flavor_name)
        status = op_utils.update_flavor_name(self.nova_client, self.flavor_name, self.flavor_name_new, self.vcpus, self.ram, self.disk)

        if status:
            LOG.info("Update flavor successful!")
        else:
            LOG.info("Update flavor failed!")

