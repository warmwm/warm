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
import subprocess
import logging

from yardstick.benchmark.scenarios import base
from yardstick.common import constants as consts
import yardstick.common.openstack_utils as op_utils

LOG = logging.getLogger(__name__)


class Server(base.Scenario):
    """Server Operation"""

    __scenario_type__ = "Server"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg

        self.action = getattr(self, self.scenario_cfg['action'])

        self.options = self.scenario_cfg['options']
        '''
        self.paras = {
            'server': self.options.get("server", None),
            'is_wait': self.options.get("wait", True),
            'reboot_type': self.options.get("reboot_type", "SOFT")
        }
        '''
        self.setup_done = False

    def setup(self):
        """scenario setup"""
        pass

    def create_server_from_volume(self, **kwargs):
        name = kwargs.get("name")
        flavor_id = kwargs.get("flavor").get("id")
        volume_id = kwargs.get("volume").get("id")
        network_id = op_utils.get_network_id2(os.getenv("EXTERNAL_NETWORK"))

        json_body = {'name': name,
                     'image': None,
                     'flavor': flavor_id,
                     'block_device_mapping_v2': [{
                         "boot_index": "0",
                         "uuid": volume_id,
                         "device_name": "vda",
                         "source_type": "volume",
                         "destination_type": "volume"
                         }],
                     'nics': [{"net-id": network_id}],
                     }
        server = op_utils.create_instance_and_wait_for_active(json_body)
        if server:
            return self._change_obj_to_dict(server)
        else:
            return None

    @staticmethod
    def delete(**kwargs):
        server_id = kwargs.get("server").get("id")
        return op_utils.delete_server(server_id)

    @staticmethod
    def start(**kwargs):
        server = kwargs.get("server", None)
        is_wait = kwargs.get("wait", True)
        LOG.debug("--Start server ID is %s", server['id'])
        return op_utils.start_server(server['id'], is_wait)

    @staticmethod
    def stop(**kwargs):
        server = kwargs.get("server", None)
        is_wait = kwargs.get("wait", True)
        LOG.debug("--Stop server ID is %s", server['id'])
        return op_utils.stop_server(server['id'], is_wait)

    @staticmethod
    def suspend(**kwargs):
        server = kwargs.get("server", None)
        is_wait = kwargs.get("wait", True)
        LOG.debug("--Suspend server ID is %s", server['id'])
        return op_utils.suspend_server(server['id'], is_wait)

    @staticmethod
    def resume(**kwargs):
        server = kwargs.get("server", None)
        is_wait = kwargs.get("wait", True)
        LOG.debug("--Resume server ID is %s", server['id'])
        return op_utils.resume_server(server['id'], is_wait)

    @staticmethod
    def pause(**kwargs):
        server = kwargs.get("server", None)
        is_wait = kwargs.get("wait", True)
        LOG.debug("--Pause server ID is %s", server['id'])
        return op_utils.pause_server(server['id'], is_wait)

    @staticmethod
    def unpause(**kwargs):
        server = kwargs.get("server", None)
        is_wait = kwargs.get("wait", True)
        LOG.debug("--Unpause server ID is %s", server['id'])
        return op_utils.unpause_server(server['id'], is_wait)

    @staticmethod
    def lock(**kwargs):
        server = kwargs.get("server", None)
        is_wait = kwargs.get("wait", True)
        LOG.debug("--Lock server ID is %s", server['id'])
        return op_utils.lock_server(server['id'], is_wait)

    @staticmethod
    def unlock(**kwargs):
        server = kwargs.get("server", None)
        is_wait = kwargs.get("wait", True)
        LOG.debug("--Unlock server ID is %s", server['id'])
        return op_utils.unlock_server(server['id'], is_wait)

    @staticmethod
    def reboot(**kwargs):
        server = kwargs.get("server", None)
        is_wait = kwargs.get("wait", True)
        reboot_type = kwargs.get("reboot_type", "SOFT")
        LOG.debug("--%s reboot server ID is %s", reboot_type, server['id'])
        return op_utils.reboot_server(server['id'], reboot_type, is_wait)

    @staticmethod
    def resize(**kwargs):
        server = kwargs.pop("server", None)
        flavor = kwargs.pop("flavor", None)
        disk_config = kwargs.pop("disk", None)
        is_wait = kwargs.pop("wait", True)
        LOG.debug("--Resize server ID is %s, flavor ID is %s", \
                  server['id'], flavor['id'])
        return op_utils.resize_server(server['id'], flavor['id'], \
                                      disk_config, is_wait, **kwargs)

    @staticmethod
    def confirm(**kwargs):
        server = kwargs.pop("server", None)
        is_wait = kwargs.get("wait", True)
        status = kwargs.get("status", "active")
        LOG.debug("--Confirm resize server ID is %s", server['id'])
        return op_utils.confirm_resize(server['id'], status, is_wait)

    @staticmethod
    def revert(**kwargs):
        server = kwargs.pop("server", None)
        is_wait = kwargs.get("wait", True)
        status = kwargs.get("status", "active")
        LOG.debug("--Revert resize server ID is %s", server['id'])
        return op_utils.revert_resize(server['id'], status, is_wait)

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        keys = self.scenario_cfg.get('output', '').split()
        ret_code = False
        try:
            ret_code = self.action(**self.options)
        except KeyError:
            LOG.error("%s server can not run the action!", self.action)

        values = [ret_code]
        return self._push_to_outputs(keys, values)
