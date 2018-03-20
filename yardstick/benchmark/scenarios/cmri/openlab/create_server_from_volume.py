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
from yardstick.common import constants as consts
import yardstick.common.openstack_utils as op_utils

LOG = logging.getLogger(__name__)


class CreateServerFromVolume(base.Scenario):
    """Create an OpenStack VM instance"""

    __scenario_type__ = "CreateServerFromVolume"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.server_name = self.options.get("server_name", "TestServer")
        self.flavor = self.options.get("flavor", None)
        self.volume_id = self.options.get("volume_id", None)
        # self.external_network = os.getenv("EXTERNAL_NETWORK")

        self.external_network = self.options.get("network", "ext-net")

        self.nova_client = op_utils.get_nova_client()
        self.neutron_client = op_utils.get_neutron_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        network_id = op_utils.get_network_id(self.neutron_client,
                                             self.external_network)

        cmd = "openstack server create %s --nic net-id=%s" % (self.server_name,
                                                              network_id)

        args_payload_list = ["flavor", "volume"]
        for argument in args_payload_list:
            try:
                cmd += " --" + argument + " " + self.options[argument]
            except KeyError:
                pass

        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 cwd='/home/opnfv/repos/yardstick')
            print(p.communicate()[0])
            LOG.info("Create server from volume successful!")
        except Exception:
            LOG.info("Create server from volume failed!")
            raise RuntimeError("Create server from volume failed!")

        op_utils.check_status("ACTIVE", self.server_name, 10, 5)

        server = op_utils.get_instance_by_name(self.nova_client, self.server_name)

        values = [server.id]
        keys = self.scenario_cfg.get('output', '').split()
        return self._push_to_outputs(keys, values)

