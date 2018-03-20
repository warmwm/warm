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
from IPy import IP

from yardstick.benchmark.scenarios import base

LOG = logging.getLogger(__name__)


class CheckIpInAddr(base.Scenario):
    """Check values between value1 and value2

    options:
        operator: equal(eq) and not equal(ne)
        value1:
        value2:
    output: check_result
    """

    __scenario_type__ = "CheckIpInAddr"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        LOG.debug("options=%s", self.options)
        value1 = str(self.options.get("IP"))
        value2 = str(self.options.get("Addr"))
        check_result = "FAIL"
        if value1 in IP(value2):
            check_result = "PASS"
        assert check_result == "PASS", ("Error %s should in%s"
                                        % (value1, value2))
        LOG.info("Check result is %s", check_result)
        try:
            keys = self.scenario_cfg.get('output', '').split()
        except KeyError:
            pass
        else:
            values = [check_result]
            return self._push_to_outputs(keys, values)

