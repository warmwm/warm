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



class DeleteUser(base.Scenario):
    """Delete a user"""

    __scenario_type__ = "DeleteUser"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.uuid = self.options.get("user_id", None)

        #self.keystone_client = op_utils.get_keystone_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        if not self.uuid:
            return

        LOG.info("Deleting user '%s'", self.uuid)

        cmd_delete = "openstack user delete %s" % (self.uuid)
        try:
            p = subprocess.Popen(cmd_delete, shell=True, stdout=subprocess.PIPE)
            print(p.communicate()[0])

            result.update({"Delete User": 1})
            LOG.info("Delete user successful!")

        except Exception:
            result.update({"Delete User": 0})
            LOG.info("Delete user failed!")
