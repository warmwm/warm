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


class CheckvCPUpin(base.Scenario):
    """Check if a server's vCPUs are pinned correctly

  Parameters
    cpu_set - set of physical cpu cores reserved for virtual machine 
        type:    string
        unit:    N/A
        default: null
    server_xml - XML configuation of the server instance
        type:    XML
        unit:    N/A
        default: null
    """

    __scenario_type__ = "CheckvCPUpin"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']
        self.server_xml = self.options.get("server_xml", None)
        self.cpu_set = self.options.get("cpu_set", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        pinning = []
        root = ET.fromstring(self.server_xml)
        for vcpupin in root.iter('vcpupin'):
            pinning.append(vcpupin.attrib)

        for item in pinning:
            assert str(item['cpuset']) in self.cpu_set, "Test failed: Server vCPU not pinned correctly!"

        LOG.info("Test passed: Server vCPU pinned correctly!")
