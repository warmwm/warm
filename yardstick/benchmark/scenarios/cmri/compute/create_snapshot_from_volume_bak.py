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
import time

LOG = logging.getLogger(__name__)


class CreateSnapshotFromVolume(base.Scenario):
    """Create an volume snapshot"""

    __scenario_type__ = "CreateSnapshotFromVolume"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.name = self.options.get("name", "TestSnapshot")
        self.volume = self.options.get("volume", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        if not self.volume:
            LOG.error("Create snapshot fail, volume None.")
            raise  RuntimeError("Create snapshot failed!")

        snapshot = op_utils.create_snapshot(self.volume, self.name)
        status = snapshot.status

        while (status == 'creating' or status == 'downloading'):
            LOG.info("Snapshot status is: %s" % status)
            time.sleep(5)
            snapshot = op_utils.get_snapshot_by_name(self.name)
            status = snapshot.status

        LOG.info("Create snapshot successful!")

        values = [snapshot.id]
        keys = self.scenario_cfg.get('output', '').split()
        return self._push_to_outputs(keys, values)