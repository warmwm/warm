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


class GetImage(base.Scenario):
    """Get an OpenStack image by name"""

    __scenario_type__ = "GetImage"


    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.image_name = self.options.get("image_name", "TestImage")

        self.glance_client = op_utils.get_glance_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        keys = self.scenario_cfg.get('output', '').split()
        values = []

        LOG.info("Querying image: %s", self.image_name)
        image = op_utils.get_image_by_name(self.glance_client, self.image_name)

        if image:
            LOG.info("Get image successful!")
            rc = 0
            values.append(rc)
            try:
                for key in keys[1:]:
                    values.append(image[key])
            except KeyError, e:
                LOG.info("KeyError: Attribute '%s' does not exist!" % str(e))
        else:
            LOG.info("Get image: no image matched!")
            rc = 1
            values.append(rc)

        return self._push_to_outputs(keys, values)
