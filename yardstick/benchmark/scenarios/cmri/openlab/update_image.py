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

LOG = logging.getLogger(__name__)


class UpdateImage(base.Scenario):
    """Update an OpenStack image"""

    __scenario_type__ = "UpdateImage"


    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.image_name = self.options.get("image_name", "TestImage")
        self.image_id = None
        self.custom_property = self.options.get("property", None) 

        self.glance_client = op_utils.get_glance_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        self.image_id = op_utils.get_image_id(self.glance_client, self.image_name)

        kwargs = {}
        args_payload_list = ["name", "min-disk", "min-ram", "tags", "kernal-id",
                             "architecture", "container-format", "disk-format",
                             "protected", "public", "activate"]

        for argument in args_payload_list:
            try:
                kwargs[argument] = self.options[argument]
            except KeyError:
                pass

        if self.custom_property:
           kwargs = dict(kwargs, **self.custom_property)

        status = op_utils.update_image(self.glance_client, self.image_id, **kwargs)

        if status:
            LOG.info("Update image successful!")
            rc = 0
        else:
            LOG.info("Update image failed!")
            rc = 1

        values = [rc]
        keys = self.scenario_cfg.get('output', '').split()
        return self._push_to_outputs(keys, values)
