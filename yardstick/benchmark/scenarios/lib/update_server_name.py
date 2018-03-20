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


class UpdateServerName(base.Scenario):
    """Update Server Name"""

    __scenario_type__ = "UpdateServerName"
    
    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg.get('options', {})

        self.server_id = self.options.get("server_id", None)
        if self.server_id:
            LOG.debug('Server id is %s', self.server_id)

        self.new_server_name = self.options.get('new_server_name')
        if self.new_server_name:
            LOG.debug('New server name is %s', self.new_server_name)

        self.nova_client = op_utils.get_nova_client()
        
        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""
        
        status = op_utils.update_server_name(self.server_id, self.new_server_name)

        if status:
            LOG.info("Update server name successful!")
        else:
            LOG.info("Update server name failed!")


