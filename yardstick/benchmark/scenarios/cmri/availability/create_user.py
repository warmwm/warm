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

import  json
import subprocess

LOG = logging.getLogger(__name__)



class CreateUser(base.Scenario):
    """Create a user"""

    __scenario_type__ = "CreateUser"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.username = self.options.get("username", 'user_test')
        self.passwd = self.options.get("passwd",'123456')
        self.uuid = None

        #self.keystone_client = op_utils.get_keystone_client()

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        LOG.info("Creating user '%s'", self.username)

        '''
        self.uuid = self.keystone_client.users.create(
            self.username, password=self.passwd)['user']['id']

        time.sleep(30)

        if not self.uuid :
            result.update({"Create User": 0})
            LOG.error("Create user '%s' failed", self.username)
            raise RuntimeError("Create user error")
        else:
            result.update({"Create User": 1})
            LOG.info("Created user '%s' success!",self.username)

        try:
            keys = self.scenario_cfg.get('output', '').split()
        except KeyError:
            pass
        else:
            values = [self.uuid]
            return self._push_to_outputs(keys, values)
        '''

        cmd_create = "openstack user create %s --password %s" % (self.username,
                                                        self.passwd)
        try:
            p = subprocess.Popen(cmd_create, shell=True, stdout=subprocess.PIPE)
            print(p.communicate()[0])
            result.update({"Create User": 1})
            LOG.info("Create user successful!")
        except Exception:
            result.update({"Create User": 0})
            LOG.info("Create user failed!")
            raise  RuntimeError("Create user failed!")

        cmd = "openstack user show -f json %s" % (self.username)

        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            user = json.loads(p.communicate()[0])
        except Exception:
            raise RuntimeError("Get user_uuid failed!")

        values = [user['id']]
        keys = self.scenario_cfg.get('output', '').split()
        return self._push_to_outputs(keys, values)