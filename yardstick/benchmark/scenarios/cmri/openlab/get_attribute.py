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


class GetAttribute(base.Scenario):
    """Get attribute of a give instance"""

    __scenario_type__ = "GetAttribute"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg.get('options', {})
        self.instance = self.options.get("target", None)

    def run(self, result):
        """execute the test"""

        keys = self.scenario_cfg.get('output', '').split()
        values = []
        
        if self.instance:
            rc = 0
            values.append(rc)
            try:
                for key in keys[1:]:
                    values.append(self.instance[key])
            except KeyError, e:
                LOG.info("KeyError: Attribute '%s' does not exist!" % str(e))
            LOG.info("Get attribute successful!")
        else:
            LOG.info("Get attribute failed: No target specified!")
            rc = 1
            values.append(rc)

        return self._push_to_outputs(keys, values)
