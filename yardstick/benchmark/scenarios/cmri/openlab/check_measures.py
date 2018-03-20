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
import time

from yardstick.benchmark.scenarios import base
import yardstick.common.openstack_utils as op_utils

LOG = logging.getLogger(__name__)


class CheckMeasures(base.Scenario):
    """Create an OpenStack flavor"""

    __scenario_type__ = "CheckMeasures"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.openstack = self.options.get("openstack_paras", None)

        self.gnocchi_client = op_utils.get_gnocchi_client()

        self.setup_done = False
        self.Value_Not = True

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()
        for i in range(0, 30):
            data = self.gnocchi_client.metric.get_measures(**self.openstack)
            LOG.debug("Waiting for metric measurement!")
            if len(data):
                self.Value_Not = False
                value = data[-1][2]
                break
            time.sleep(60)

        if self.Value_Not:
            LOG.exception("Timeout measure value")

        if value:
            result.update({self.openstack["metric"]: value})
            LOG.info("Measure value successful, value is %s" % value)
        else:
            result.update({self.openstack["metric"]: "error"})
            LOG.error("Measure value failed!")

        try:
            keys = self.scenario_cfg.get('output', '').split()
        except KeyError:
            pass
        else:
            values = [value]
            return self._push_to_outputs(keys, values)

