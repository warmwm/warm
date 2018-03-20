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

LOG = logging.getLogger(__name__)



class DeleteSnapshot(base.Scenario):
    """Delete a snapshot"""

    __scenario_type__ = "DeleteSnapshot"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.snapshot_id = self.options.get("snapshot_id", None)

        self.cinder_client = op_utils.get_cinder_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        if not self.snapshot_id:
            LOG.error("snapshot_id is None.")
            raise RuntimeError("Delete snapshot failed!")

        status = op_utils.delete_snapshot(self.cinder_client, self.snapshot_id)

        if status:
            LOG.info("Delete snapshot successful!")
        else:
            LOG.info("Delete snapshot failed!")
