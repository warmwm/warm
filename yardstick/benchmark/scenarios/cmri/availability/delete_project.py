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



class DeleteProject(base.Scenario):
    """Delete a project"""

    __scenario_type__ = "DeleteProject"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.ids = self.options.get("project_ids", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        if not self.ids:
            return

        for id in self.ids:
            LOG.info("Deleting project '%s'", id)

            cmd_delete = "openstack project delete %s" % (id)
            try:
                p = subprocess.Popen(cmd_delete, shell=True, stdout=subprocess.PIPE)
                print(p.communicate()[0])

            except Exception:
                result.update({"Delete porject": 0})
                LOG.info("Delete project failed!")

        result.update({"Delete project": 1})
        LOG.info("Delete project successful!")
