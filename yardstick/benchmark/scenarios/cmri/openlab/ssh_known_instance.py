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
import yardstick.ssh as ssh
import os

from yardstick.benchmark.scenarios import base
import yardstick.common.constants as yardstick_path

LOG = logging.getLogger(__name__)


class sshKnownInstance(base.Scenario):
    """Ssh to an OpenStack floating ip"""

    __scenario_type__ = "sshKnownInstance"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        try:
            self.floating_ip_addr = self.options['floating_ip_addr']
        except KeyError:
            try:
                host = self.context_cfg['host']
            except KeyError:
                raise
            else:
                self.ssh_user = host.get('user', 'ubuntu')
                self.ssh_port = host.get("ssh_port", 22)
                self.floating_ip_addr = host.get('ip', None)
                self.sshkey = host.get('key_filename', '/root/.ssh/id_rsa')
                self.ssh_passwd = host.get('password', None)
                self.ssh_time = 600
        else:
            self.sshkey = self.options.get("sshkey", None)
            self.ssh_passwd = self.options.get("ssh_passwd", None)
            self.ssh_user = self.options.get("ssh_user", None)
            self.ssh_port = self.options.get("ssh_port", 22)
            self.ssh_time = self.options.get("ssh_timeout", 600)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True
        if self.ssh_passwd is not None:
            LOG.info("Log in via pw, user:%s, host:%s, pw:%s",
                     self.ssh_user, self.floating_ip_addr, self.ssh_passwd)
            self.connection = ssh.SSH(self.ssh_user,
                                      self.floating_ip_addr,
                                      password=self.ssh_passwd,
                                      port=self.ssh_port)
        else:
            LOG.info("Log in via key, user:%s, host:%s, key_filename:%s",
                     self.ssh_user, self.floating_ip_addr, self.sshkey)
            self.connection = ssh.SSH(self.ssh_user,
                                      self.floating_ip_addr,
                                      key_filename=self.sshkey,
                                      port=self.ssh_port)

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        try:
            file_path = self.options['file']
        except KeyError:
            pass
        else:
            try:
                self.connection.wait(timeout=self.ssh_time)
                file_path = os.path.join(yardstick_path.YARDSTICK_ROOT_PATH,
                                         file_path)
                with open(file_path, "rb") as file_benchmark:
                    self.connection.run("cat > ~/benchmark.sh",
                                        stdin=file_benchmark)
                cmd = "sudo sh benchmark.sh"
                parameter = self.options.get('parameter')
                if parameter is not None:
                    for value in parameter:
                        cmd += (" %s" % value)
                status, stdout, stderr = self.connection.execute(cmd)
            except ssh.SSHTimeout:
                status = 1
                stdout = 1

        try:
            cmd = self.options['cmd']
        except KeyError:
            pass
        else:
            try:
                self.connection.wait(timeout=self.ssh_time)
                cmd = 'sudo {}'.format(cmd)
                status, stdout, stderr = self.connection.execute(cmd)
            except ssh.SSHTimeout:
                status = 1
                stdout = 1
            stdout = stdout.replace('\n', '')

        if status:
            result.update({"ssh_result": 0})
        else:
            result.update({"ssh_result": 1})

        keys = self.scenario_cfg.get('output', '').split()
        values = [status, stdout]
        return self._push_to_outputs(keys, values)
