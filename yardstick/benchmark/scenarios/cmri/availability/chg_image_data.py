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



class ChgImageData(base.Scenario):
    """Change Image Metadata"""

    __scenario_type__ = "ChgImageData"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.image_name = self.options.get("image_name", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        if not self.image_name:
            return

        LOG.info("Change Image Metadata")

        cmd_set = "openstack image set %s --property hw_cpu_max_sockets=2 --property hw_cpu_max_threads=1" % (self.image_name)
        try:
            p = subprocess.Popen(cmd_set, shell=True, stdout=subprocess.PIPE)
            print(p.communicate()[0])

        except Exception:
            result.update({"Change Image Metadata": 0})
            LOG.info("Change Image Metadata failed!")

        result.update({"Change Image Metadata": 1})
        LOG.info("Change Image Metadata successful!")
