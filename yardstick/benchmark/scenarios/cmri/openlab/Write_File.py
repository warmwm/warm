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

LOG = logging.getLogger(__name__)


class WriteFile(base.Scenario):
    """Check values between value1 and value2

    options:
        operator: equal(eq) and not equal(ne)
        value1:
        value2:
    output: check_result
    """

    __scenario_type__ = "WriteFile"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.str = self.options.get("str", None)
        self.file_local = self.options.get("file_local", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        LOG.debug("options=%s", self.options)
        with open(self.file_local, 'wb') as f:
            f.write(self.str)

        LOG.info("Write file result is Successful")
        LOG.info("%s string local at %s", self.str, self.file_local)

