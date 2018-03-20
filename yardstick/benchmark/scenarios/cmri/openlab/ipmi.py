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
import subprocess

from yardstick.benchmark.scenarios import base
from yardstick.common import constants as consts
import yardstick.common.openstack_utils as op_utils

LOG = logging.getLogger(__name__)


class IPMI(base.Scenario):
    """Manage host system via IPMI"""

    __scenario_type__ = "IPMI"


    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.host = self.options.get("host", None)
        self.ipmi_ip = self.options.get("ipmi_ip", None)
        self.ipmi_user = self.options.get("ipmi_user", "root")
        self.ipmi_pwd = self.options.get("ipmi_pwd", "root")
        self.action = self.options.get("action", None)
        self.ipmi_pool = self.options.get("ipmi_pool", {})

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        if self.host and self.ipmi_ip is None:
            self.ipmi_ip = self.ipmi_pool.get(self.host)

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        cmd = "ipmitool -I lanplus -H %s -U %s -P %s %s" \
               % (self.ipmi_ip, self.ipmi_user, self.ipmi_pwd, self.action)

        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 cwd=consts.YARDSTICK_REPOS_DIR)
            print(p.communicate()[0])
            LOG.info("%s hoet system successful!", self.action)
            rc = 0
        except Exception:
            LOG.info("%s host system failed!", self.action)
            rc = 1

        values = [rc]
        keys = self.scenario_cfg.get('output', '').split()
        return self._push_to_outputs(keys, values)
