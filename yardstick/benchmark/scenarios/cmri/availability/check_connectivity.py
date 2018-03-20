##############################################################################
# Copyright (c) 2017 CMRI
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

from yardstick.benchmark.scenarios import base

LOG = logging.getLogger(__name__)


class CheckConnectivity(base.Scenario):
    """Check connectivity between two instances"""

    __scenario_type__ = "CheckConnectivity"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.sshkey = self.options.get("sshkey", None)
        self.ssh_passwd = self.options.get("ssh_passwd", None)
        self.ssh_user = self.options.get("ssh_user", None)
        self.ssh_port = self.options.get("ssh_port", 22)
        self.ssh_time = self.options.get("ssh_timeout", 600)

        self.source_ip_addr = self.options.get("src_ip_addr", None)
        self.dest_ip_addr = self.options.get("dest_ip_addr", None)

        self.setup_done = False
        self.connection = None

    def setup(self):
        """scenario setup"""

        self.setup_done = True
        if self.ssh_passwd is not None:
            LOG.info("Log in via pw, user:%s, host:%s, pw:%s",
                     self.ssh_user, self.source_ip_addr, self.ssh_passwd)
            self.connection = ssh.SSH(self.ssh_user,
                                      self.source_ip_addr,
                                      password=self.ssh_passwd,
                                      port=self.ssh_port)
        else:
            LOG.info("Log in via key, user:%s, host:%s, key_filename:%s",
                     self.ssh_user, self.source_ip_addr, self.sshkey)
            self.connection = ssh.SSH(self.ssh_user,
                                      self.source_ip_addr,
                                      key_filename=self.sshkey,
                                      port=self.ssh_port)


    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        try:
            self.connection.wait(timeout=self.ssh_time)
        except ssh.SSHTimeout:
            raise
        else:
            try:
                # ping -c 4 -s 1473 -M do 192.168.115.6
                cmd = 'ping -c 4 ' + self.dest_ip_addr
                parameter = self.options.get('parameter', None)
                if parameter:
                    cmd += (" %s" % parameter)

                status, stdout, stderr = self.connection.execute(cmd)
                LOG.info("CMD: %s", cmd)
                LOG.info("ping %s ==> %s", self.source_ip_addr, self.dest_ip_addr)
                LOG.info("%s", stdout)
            
                if "sla" in self.scenario_cfg:
                    conn_status = self.scenario_cfg['sla']['status']
                    if status != 0:
                        LOG.info("%s", stderr)
                        assert not conn_status , "%s ==> %s" % \
                            (self.source_ip_addr, self.dest_ip_addr)
                    else:
                        assert conn_status , "%s =/=> %s" % \
                            (self.source_ip_addr, self.dest_ip_addr)
            except KeyError:
                pass
            except AssertionError:
                result.update({"Check_Connectivity": 0})   
            else:
                result.update({"Check_Connectivity": 1})   

