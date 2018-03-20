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
import xml.etree.ElementTree as ET

import yaml

import yardstick.ssh as ssh
from yardstick.benchmark.scenarios import base
from yardstick.common import constants as consts
from yardstick.common.task_template import TaskTemplate

LOG = logging.getLogger(__name__)


class CheckNUMA(base.Scenario):
    """Check if vcpus are pinned to a NUMA node correctly"""

    __scenario_type__ = "CheckNUMA"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']
        self.server_id = self.options.get("server_id", None)

        self.node_type = self.options.get("node_type", None)
        self.host_str = self.options.get("host", None)
        self.host_list = self.host_str.split(',')

        self.ssh_client = None

        node_file = os.path.join(consts.YARDSTICK_ROOT_PATH,
                                 self.options.get("file"))

        with open(node_file) as f:
            nodes = yaml.safe_load(TaskTemplate.render(f.read()))
        self.nodes = {a['name']: a for a in nodes['nodes']}

        self.setup_done = False

    def _get_host_node(self, hosts, node_type):
        # get node for given node type
        nodes = [a for a in hosts if self.nodes.get(a, {}).get('role') ==
                 node_type]
        if not nodes:
            LOG.error("Can't find %s node in the context!!!", node_type)
        return nodes

    def _ssh_host(self, node_name):
        # ssh host
        node = self.nodes.get(node_name, None)
        user = str(node.get('user', 'ubuntu'))
        ssh_port = str(node.get("ssh_port", ssh.DEFAULT_PORT))
        ip = str(node.get('ip', None))
        pwd = node.get('password', None)
        key_fname = node.get('key_filename', '/root/.ssh/id_rsa')
        if pwd is not None:
            LOG.debug("Log in via pw, user:%s, host:%s, password:%s",
                      user, ip, pwd)
            self.ssh_client = ssh.SSH(user, ip, password=pwd, port=ssh_port)
        else:
            LOG.debug("Log in via key, user:%s, host:%s, key_filename:%s",
                      user, ip, key_fname)
            self.ssh_client = ssh.SSH(user, ip, key_filename=key_fname,
                                      port=ssh_port)
        self.ssh_client.wait(timeout=600)

    def setup(self):
        """scenario setup"""

        # log in an Openstack node
        self.node_name = self._get_host_node(self.host_list, self.node_type)
        LOG.debug("The %s Node is: %s", self.node_type, self.node_name)
        for node in self.node_name:
            self._ssh_host(node)

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        cmd = "sudo virsh dumpxml %s" % self.server_id
        LOG.debug("Dumping VM configrations: %s", cmd)
        status, stdout, stderr = self.ssh_client.execute(cmd)
        if status:
            raise RuntimeError(stderr)

        pinning = []
        root = ET.fromstring(stdout)
        for memnode in root.iter('memnode'):
            pinning.append(memnode.attrib)

        if len(pinning) == 1:
            LOG.info("Test passed: NUMA pinned correctly!")
        else:
            LOG.info("Test failed!")
