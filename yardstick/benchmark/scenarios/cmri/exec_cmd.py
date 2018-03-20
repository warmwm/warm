##############################################################################
# Copyright (c) 2015 Ericsson AB and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# ping scenario

from __future__ import print_function
from __future__ import absolute_import
import pkg_resources
import logging

import yardstick.ssh as ssh
from yardstick.common import utils
from yardstick.benchmark.scenarios import base

LOG = logging.getLogger(__name__)


class ExecuteCommand(base.Scenario):
    """execute Linux command on the node or vm

  Parameters
    command - the command to execute
        type:    string
        default: 'ls'
    """

    __scenario_type__ = "ExecuteCommand"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
	self.command = self.scenario_cfg['options'].get("command", 'ls')
	host = self.scenario_cfg['options'].get("host", '')
	user = self.scenario_cfg['options'].get("user", '')
	password = self.scenario_cfg['options'].get("password", '')
        # self.connection = ssh.SSH(host=host, user=user, password=password)
	print('+++++++++++++++++++++++')
        print(host)
	self.connection = ssh.SSH.from_node(host, defaults={"root": "root"})
        self.connection.wait(timeout=600)

    def run(self, result):
        """execute the command """

	exit_status, stdout, stderr = self.connection.execute(self.command)
	if exit_status != 0:
		raise RuntimeError(stderr)
	if stdout:
		print(stdout)
        # result.update(('exit_status', exit_status))


def _test():    # pragma: no cover
    """internal test function"""
    key_filename = pkg_resources.resource_filename("yardstick.resources",
                                                   "files/yardstick_key")
    ctx = {
        "host": {
            "ip": "10.229.47.137",
            "user": "root",
            "key_filename": key_filename
        },
        "target": {
            "ipaddr": "10.229.17.105",
        }
    }

    logger = logging.getLogger("yardstick")
    logger.setLevel(logging.DEBUG)

    args = {}
    result = {}

    p = Ping(args, ctx)
    p.run(result)
    print(result)


if __name__ == '__main__':    # pragma: no cover
    _test()
