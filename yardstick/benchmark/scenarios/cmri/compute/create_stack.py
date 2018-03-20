##############################################################################
# Copyright (c) 2017 CMRI.
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



class CreateStack(base.Scenario):
    """Create a stack from template data"""

    __scenario_type__ = "CreateStack"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.stack_name = self.options.get("name", 'stack_test')
        self.timeout = self.options.get("timeout", 60)
        self.template_data = self.options.get("template_data", None)

        self.heat_client = op_utils.get_heat_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def status(self):
        """returns stack state as a string"""
        heat_client = self.heat_client
        stack = heat_client.stacks.get(self.uuid)
        return stack.stack_status

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        LOG.info("Creating stack '%s'", self.stack_name)

        start_time = time.time()
        self.uuid = self.heat_client.stacks.create(
            stack_name=self.stack_name,
            template=self.template_data)['stack']['id']

        time_limit = start_time + self.timeout
        for status in iter(self.status, u'CREATE_COMPLETE'):
            LOG.info("stack state %s", status)
            if status == u'CREATE_FAILED':
                stack_status_reason = self.heat_client.stacks.get(self.uuid).stack_status_reason
                self.heat_client.stacks.delete(self.uuid)
                raise RuntimeError(stack_status_reason)
            if time.time() > time_limit:
                raise RuntimeError("Heat stack create timeout")

            time.sleep(2)

        end_time = time.time()
        outputs = self.heat_client.stacks.get(self.uuid).outputs

        result.update({"Create Stack": 1})
        LOG.info("Created stack '%s' in %.3e secs",
                 self.stack_name, end_time - start_time)

        try:
            keys = self.scenario_cfg.get('output', '').split()
        except KeyError:
            pass
        else:
            values = [self.uuid]
            return self._push_to_outputs(keys, values)
