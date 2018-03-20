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

import yaml

import yardstick.ssh as ssh
from yardstick.benchmark.scenarios import base
from yardstick.common import constants as consts
import yardstick.common.openstack_utils as op_utils
from yardstick.common.task_template import TaskTemplate

LOG = logging.getLogger(__name__)


class GetServerXmlConf(base.Scenario):
    """Get a server's XML configuration file
    
  Parameters
    server - instance of the server
        type:    dict
        unit:    N/A
        default: null
    pod_file - path to pod configuration file
        type:    string
        unit:    N/A
        default: null

  Outputs:
    server_xml - XML configuation of the server instance
        type:    XML
        unit:    N/A
    """

    __scenario_type__ = "GetServerXmlConf"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']
        self.server = self.options.get("server")
        self.server_id = self.server["id"]
        self.server_host = self.server["OS-EXT-SRV-ATTR:host"]
        self.connection = None

        pod_file = os.path.join(consts.YARDSTICK_ROOT_PATH,
                                 self.options.get("pod_file"))
        with open(pod_file) as f:
            nodes = yaml.safe_load(TaskTemplate.render(f.read()))
        self.nodes = {a['host_name']: a for a in nodes['nodes']}

        self.setup_done = False

    def _ssh_host(self, server_host):
        """establish a ssh connection to the host node"""

        # ssh host
        node = self.nodes.get(server_host, None)
        user = str(node.get('user', 'ubuntu'))
        ssh_port = str(node.get("ssh_port", ssh.DEFAULT_PORT))
        ip = str(node.get('ip', None))
        pwd = node.get('password', None)
        key_fname = node.get('key_filename', '/root/.ssh/id_rsa')
        if pwd is not None:
            LOG.debug("Log in via pw, user:%s, host:%s, password:%s",
                      user, ip, pwd)
            self.connection = ssh.SSH(user, ip, password=pwd, port=ssh_port)
        else:
            LOG.debug("Log in via key, user:%s, host:%s, key_filename:%s",
                      user, ip, key_fname)
            self.connection = ssh.SSH(user, ip, key_filename=key_fname,
                                  port=ssh_port)
        self.connection.wait(timeout=600)

    def setup(self):
        """scenario setup"""

        self._ssh_host(self.server_host)

        self.setup_done = True

    def run(self, result):
        """execute the benchmark"""

        if not self.setup_done:
            self.setup()

        cmd = "sudo virsh dumpxml %s" % self.server_id
        LOG.debug("Dumping server's XML configration file: %s", cmd)
        status, stdout, stderr = self.connection.execute(cmd)
        if status:
            raise RuntimeError(stderr)

        LOG.info("Get server's XML configuration file successful!")
        
        values = [stdout]
        keys = self.scenario_cfg.get('output', '').split()
        return self._push_to_outputs(keys, values)
