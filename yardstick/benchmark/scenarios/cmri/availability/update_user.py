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



class UpdateUser(base.Scenario):
    """Update a user"""

    __scenario_type__ = "UpdateUser"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.uuid = self.options.get('user_id', None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        LOG.info("Updating user '%s'", self.uuid)

        if not self.uuid:
            return

        cmd_update = "openstack user set %s  " % (self.uuid)

        args_payload_list = ["name", "password", "email", "description"]
        for argument in args_payload_list:
            try:
                cmd_update += " --" + argument + " " + self.options[argument]
            except KeyError:
                pass

        try:
            p = subprocess.Popen(cmd_update, shell=True, stdout=subprocess.PIPE)
            print(p.communicate()[0])

            result.update({"Update User": 1})
            LOG.info("Update user successful!")

        except Exception:
            result.update({"Update User": 0})
            LOG.info("Update user failed!")
