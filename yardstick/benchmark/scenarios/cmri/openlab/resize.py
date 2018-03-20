# ############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
# ############################################################################

from __future__ import print_function
from __future__ import absolute_import

import logging
import time
from datetime import datetime

from yardstick.benchmark.scenarios import base
from yardstick.common import openstack_utils

LOG = logging.getLogger(__name__)


class Resize(base.Scenario):
    """Execute a cold migration for two hosts

  Parameters
    server_id - ID of the server
        type:    string
        unit:    N/A
        default: null
    server- dict of the server
        type:    dict
        unit:    N/A
        default: null
    Either server_id or server is required.

    flavor_id - ID of the flavor
        type:    string
        unit:    N/A
        default: null
    flavor- dict of the flavor
        type:    dict
        unit:    N/A
        default: null
    Either flavor_id or flavor is required.

  Outputs
    rc - response code of resize operation
        0 for success
        1 for failure
        type:    int
        unit:    N/A
    resize_time - the duration time resize operation used
        type:    float
        unit:    N/A
        default: null
    error_message - the error message(only if fail to resize)
        type:    string
        unit:    N/A
        default: null

    """

    __scenario_type__ = "RESIZE"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.options = self.scenario_cfg.get('options', {})
        self.nova_client = openstack_utils.get_nova_client()

    def run(self, result):

        default_server_id = self.options.get('server', {}).get('id', '')
        server_id = self.options.get('server_id', default_server_id)
        default_flavor_id = self.options.get('flavor', {}).get('id', '')
        flavor_id = self.options.get('flavor_id', default_flavor_id)
        LOG.debug('Server id is %s, Flavor id is %s', server_id, flavor_id)

        keys = self.scenario_cfg.get('output', '').split()

        LOG.info('Start to resize')
        try:
            self.nova_client.servers.resize(server_id, flavor_id)
        except Exception as e:
            values = [1, str(e).split('.')[0]]
        else:
            start_time = datetime.now()
            self._wait_check_status(server_id, 'verify_resize')
            LOG.info('Server status change to VERIFY_RESIZE')

            LOG.info('Start to comfirm resize')
            self.nova_client.servers.confirm_resize(server_id)

            self._wait_check_status(server_id, 'active')
            LOG.info('Server status change to ACTIVE')
            end_time = datetime.now()

            LOG.info('Resize successful')
            duration = end_time - start_time
            resize_time = duration.seconds + duration.microseconds * 1.0 / 1e6
            values = [0, resize_time]

        return self._push_to_outputs(keys, values)

    def _wait_check_status(self, server_id, wait_status):
        while True:
            status = self.nova_client.servers.get(server_id).status.lower()
            if status == wait_status:
                break
            time.sleep(1)
