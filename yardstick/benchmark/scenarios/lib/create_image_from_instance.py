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


class CreateImageFromInstance(base.Scenario):
    """Create Image From Instance"""

    __scenario_type__ = "CreateImageFromInstance"
    
    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg.get('options', {})

        self.server_id = self.options.get("server_id", None)
        if self.server_id:
            LOG.debug('Server id is %s', self.server_id)

        self.image_name = self.options.get('image_name')
        if self.image_name:
            LOG.debug('Image name is %s', self.image_name)
        
        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""
        
        image_id = op_utils.create_image_from_instance(self.server_id, self.image_name)

        if image_id:
            LOG.info("Create image successful!")
            values = [image_id]

        else:
            LOG.info("Create image failed!")
            values = []

        keys = self.scenario_cfg.get('output', '').split()
        return self._push_to_outputs(keys, values)


