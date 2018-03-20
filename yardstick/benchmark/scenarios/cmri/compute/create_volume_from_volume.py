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


class CreateVolumeFromVolume(base.Scenario):
    """Create an volume from volume"""

    __scenario_type__ = "CreateVolumeFromVolume"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.name = self.options.get("name", "TestSnapshot")
        self.size = self.options.get("size", 5)
        self.volume_id = self.options.get("volume_id", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        if not self.volume_id:
            LOG.error("Create volume failed.")
            raise  RuntimeError("Create volume failed!")

        volume = op_utils.create_volume_from_volume(self.name,
                                                        self.size,
                                                        self.volume_id)

        status = volume.status

        while (status == 'creating' or status == 'downloading'):
            LOG.info("Volume status is: %s" % status)
            time.sleep(5)
            volume = op_utils.get_volume_by_name(self.name)
            status = volume.status

        LOG.info("Create volume successful!")

        values = [volume.id]
        keys = self.scenario_cfg.get('output', '').split()
        return self._push_to_outputs(keys, values)
