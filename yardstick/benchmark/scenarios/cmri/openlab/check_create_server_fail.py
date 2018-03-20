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

from yardstick.benchmark.scenarios import base
import yardstick.common.openstack_utils as op_utils

LOG = logging.getLogger(__name__)


class CheckCreateServerFail(base.Scenario):
    """Verify create server failed in some condition

  Parameters
    image - name of the image
        type:    string
        unit:    N/A
        default: null

    """

    __scenario_type__ = "CheckCreateServerFail"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']
        self.image = self.options.get("image", 'cirros-0.3.5')
        self.external_network = os.getenv("EXTERNAL_NETWORK")
        self.nova_client = op_utils.get_nova_client()
        self.neutron_client = op_utils.get_neutron_client()
        self.glance_client = op_utils.get_glance_client()
        self.instance = None

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the benchmark"""

        if not self.setup_done:
            self.setup()

        network_id = op_utils.get_network_id(self.neutron_client,
                                             self.external_network)
        image_id = op_utils.get_image_id(self.glance_client, self.image)
        flavor_id = op_utils.get_flavor_id(self.nova_client,
                                           "yardstick-pinned-flavor")

        # Create multiple VMs to test CPU ran out
        LOG.debug("Creating server instance: test_server")
        json_body = {'flavor': flavor_id,
                     'image': image_id,
                     'nics': [{"net-id": network_id}],
                     'name': "test_server"}
        self.instance = op_utils.create_instance(json_body)

        status = op_utils.check_status("ERROR", "test_server",
                                       10, 5)

        if status:
            LOG.info("Create test_server failed: lack of resources.")
        else:
            LOG.info("Create test_server successful.")

        op_utils.delete_instance(self.nova_client, self.instance.id)
