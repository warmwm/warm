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



class DeleteStack(base.Scenario):
    """Delete a stack"""

    __scenario_type__ = "DeleteStack"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.uuid = self.options.get("stack_id", None)
        self.timeout = self.options.get("timeout", 60)

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

        if not self.uuid:
            LOG.error("Stack_uuid is None.")
            raise RuntimeError("Delete Stack failed!")

        LOG.info("Deleting stack uuid: '%s'", self.uuid)
        heat = self.heat_client
        stack = heat.stacks.get(self.uuid)
        start_time = time.time()
        stack.delete()

        for status in iter(self.status, u'DELETE_COMPLETE'):
            LOG.info("stack state %s", status)
            if status == u'DELETE_FAILED':
                result.update({"Delete Stack": 0})
                raise RuntimeError(
                    heat.stacks.get(self.uuid).stack_status_reason)

            time.sleep(2)

        end_time = time.time()

        result.update({"Delete Stack": 1})
        LOG.info("Deleted stack uuid: '%s' in %d secs", self.uuid,
                 end_time - start_time)
