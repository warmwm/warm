##############################################################################
# Copyright (c) 2017 CMRI.
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
import time
import subprocess

LOG = logging.getLogger(__name__)



class GetServerInfo(base.Scenario):
    """Get Server Info"""

    __scenario_type__ = "GetServerInfo"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.server_name = self.options.get("server_name", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        if not self.server_name:
            return

        LOG.info("Get Server Info")

        cmd = "openstack server show %s" % (self.server_name)
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            print(p.communicate()[0])

        except Exception:
            result.update({"Get Server Info": 0})
            LOG.info("Get Server Info failed!")

        result.update({"Get Server Info": 1})
        LOG.info("Get Server Info successful!")
