##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# Qos rebind scenario
# iperf3 homepage at: http://software.es.net/iperf/

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import time
import logging
import subprocess
from oslo_serialization import jsonutils

import yardstick.ssh as ssh
from yardstick.common import constants as config
from yardstick.benchmark.scenarios import base
from yardstick.common import constants as consts
import yardstick.common.openstack_utils as op_utils
from yardstick.common.task_template import TaskTemplate


LOG = logging.getLogger(__name__)


class QoSBind(base.Scenario):
    """Execute iperf3 between two hosts with QoS policy to verify QoS control
    works.

    By default TCP is used but UDP can also be configured.
    For more info see http://software.es.net/iperf

    Parameters
    bytes - number of bytes to transmit
      only valid with a non duration runner, mutually exclusive with blockcount
        type:    int
        unit:    bytes
        default: 56
    udp - use UDP rather than TCP
        type:    bool
        unit:    na
        default: false
    nodelay - set TCP no delay, disabling Nagle's Algorithm
        type:    bool
        unit:    na
        default: false
    blockcount - number of blocks (packets) to transmit,
      only valid with a non duration runner, mutually exclusive with bytes
        type:    int
        unit:    bytes
        default: -
    """

    __scenario_type__ = "QoS_Bind"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']
        self.qos_policy = self.options.get("qos_policy", '200Mbps')
        self.bandwidth_limit = int(filter(str.isdigit, self.qos_policy))
        self.neutron_client = op_utils.get_neutron_client()
        self.setup_done = False

    def setup(self):
        """scenario setup"""

        host = self.context_cfg['host']
        host_user = host.get('user', 'ubuntu')
        host_ssh_port = host.get('ssh_port', ssh.DEFAULT_PORT)
        host_ip = host.get('ip', None)
        host_key_filename = host.get('key_filename', '~/.ssh/id_rsa')
        target = self.context_cfg['target']
        target_user = target.get('user', 'ubuntu')
        target_ssh_port = target.get('ssh_port', ssh.DEFAULT_PORT)
        target_ip = target.get('ip', None)
        target_key_filename = target.get('key_filename', '~/.ssh/id_rsa')

        LOG.info("user:%s, target:%s", target_user, target_ip)
        self.target = ssh.SSH(target_user, target_ip,
                              key_filename=target_key_filename,
                              port=target_ssh_port)
        self.target.wait(timeout=600)

        LOG.info("user:%s, host:%s", host_user, host_ip)
        self.host = ssh.SSH(host_user, host_ip,
                            key_filename=host_key_filename, port=host_ssh_port)
        self.host.wait(timeout=600)

        cmd = "iperf3 -s -D"
        LOG.debug("Starting iperf server with command: %s", cmd)
        status, _, stderr = self.target.execute(cmd)
        if status:
            raise RuntimeError(stderr)

        self.setup_done = True

    def run(self, result):
        """execute the benchmark"""
        if not self.setup_done:
            self.setup()

        cmd = "iperf3 -c %s --json" % (self.context_cfg['target']['ipaddr'])

        # Associate the created policy with an existing neutron port
        host_port_id = \
            op_utils.get_port_id_by_ip(self.neutron_client,
                                       self.context_cfg['host']['private_ip'])

        port_cmd = "neutron port-update " + host_port_id + " --qos-policy " + \
            self.qos_policy
        p = subprocess.Popen(port_cmd, shell=True, stdout=subprocess.PIPE,
                             cwd=config.YARDSTICK_REPOS_DIR)
        time.sleep(10)

        LOG.debug("Executing command: %s", cmd)
        status, stdout, stderr = self.host.execute(cmd)
        if status:
            # error cause in json dict on stdout
            raise RuntimeError(stdout)

        # Note: convert all ints to floats in order to avoid
        # schema conflicts in influxdb. We probably should add
        # a format func in the future.
        result.update(jsonutils.loads(stdout, parse_int=float))
        bandwidth1 = int(result["end"]["sum_received"]["bits_per_second"]) / 1000000

        port_cmd = "neutron port-update " + host_port_id + " --no-qos-policy"
        p = subprocess.Popen(port_cmd, shell=True, stdout=subprocess.PIPE,
                             cwd=config.YARDSTICK_REPOS_DIR)
        time.sleep(10)

        LOG.debug("Executing command: %s", cmd)
        status, stdout, stderr = self.host.execute(cmd)
        if status:
            # error cause in json dict on stdout
            raise RuntimeError(stdout)

        # Note: convert all ints to floats in order to avoid
        # schema conflicts in influxdb. We probably should add
        # a format func in the future.
        result.update(jsonutils.loads(stdout, parse_int=float))
        bandwidth2 = int(result["end"]["sum_received"]["bits_per_second"]) / 1000000


        port_cmd = "neutron port-update " + host_port_id + " --qos-policy " + \
            self.qos_policy
        p = subprocess.Popen(port_cmd, shell=True, stdout=subprocess.PIPE,
                             cwd=config.YARDSTICK_REPOS_DIR)
        time.sleep(10)

        LOG.debug("Executing command: %s", cmd)
        status, stdout, stderr = self.host.execute(cmd)
        if status:
            # error cause in json dict on stdout
            raise RuntimeError(stdout)

        # Note: convert all ints to floats in order to avoid
        # schema conflicts in influxdb. We probably should add
        # a format func in the future.
        result.update(jsonutils.loads(stdout, parse_int=float))
        bandwidth3 = int(result["end"]["sum_received"]["bits_per_second"]) / 1000000

        if 0.8 < bandwidth1/self.bandwidth_limit < 1.2 and \
            1.2 < bandwidth2/self.bandwidth_limit and \
            0.8 < bandwidth3/self.bandwidth_limit < 1.2:
            LOG.info("QoS policy works!")
        else:
            LOG.info("QoS policy dose not work!")

    def teardown(self):
        """teardown the benchmark"""
        LOG.debug("teardown")
        self.host.close()
        status, stdout, stderr = self.target.execute("pkill iperf")
        if status:
            LOG.warning(stderr)
        self.target.close()
