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

import os
import logging
import xml.etree.ElementTree as ET

import yaml

import yardstick.ssh as ssh
from yardstick.benchmark.scenarios import base
from yardstick.common import constants as consts
from yardstick.common.task_template import TaskTemplate

LOG = logging.getLogger(__name__)


class CheckNUMApin(base.Scenario):
    """Check if a server's vCPUs are pinned to the same NUMA node

  Parameters
    server_xml - XML configuation of the server instance
        type:    XML
        unit:    N/A
        default: null
    """
    __scenario_type__ = "CheckNUMApin"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']
        self.server_xml = self.options.get("server_xml", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        pinning = []
        root = ET.fromstring(self.server_xml)
        for memnode in root.iter('memnode'):
            pinning.append(memnode.attrib)

        if len(pinning) == 1:
            LOG.info("Test passed: Server NUMA pinned correctly!")
        else:
            LOG.info("Test failed: Server NUMA not pinned correctly!")
