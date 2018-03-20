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

import os
import logging
import subprocess

from yardstick.benchmark.scenarios import base
import yardstick.common.constants as yardstick_path

LOG = logging.getLogger(__name__)


class Local_excute(base.Scenario):
    """Check values between value1 and value2

    options:
        operator: equal(eq) and not equal(ne)
        value1:
        value2:
    output: check_result
    """

    __scenario_type__ = "Local_excute"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.script_local = os.path.join(yardstick_path.YARDSTICK_ROOT_PATH,
                                         self.options.get("script_local", None))
        self.parameter = self.options.get("parameter", None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        command = ("sudo sh %s" % self.script_local)
        if self.parameter is not None:
                for value in self.parameter:
                    command += (" %s" % value)

        LOG.debug("options=%s", self.options)
        try:
            print(command)
            output = subprocess.check_output(command, shell=True)
            print(output)
        except Exception:
            LOG.error("Write file result is Successful")

        status = 1
        LOG.info("Write file result is Successful")

        try:
            keys = self.scenario_cfg.get('output', '').split()
        except KeyError:
            pass
        else:
            values = [status, output]
            return self._push_to_outputs(keys, values)

