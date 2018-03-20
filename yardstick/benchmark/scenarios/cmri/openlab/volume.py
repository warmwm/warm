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

from yardstick.benchmark.scenarios import base
import yardstick.common.openstack_utils as op_utils

LOG = logging.getLogger(__name__)


class Volume(base.Scenario):
    """Get an OpenStack flavor by name"""

    __scenario_type__ = "Volume"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg

        self.action = getattr(self, self.scenario_cfg['action'])
        self.options = self.scenario_cfg['options']
        '''
        self.paras = {
            'name': self.options.get("name", "yardstick_test_flavor"),
            'ram': self.options.get("ram", 0),
            'vcpus': self.options.get("vcpus", 0),
            'disk': self.options.get("disk", 0),
            'is_public': self.options.get("is_public", True),
            'flavor': self.options.get("flavor", None)
        }
        '''
        self.setup_done = False

    def setup(self):
        """scenario setup"""
        pass

    def create(self, **kwargs):
        """create a volume"""
        name = kwargs.pop("name", "yardstick_test_volume")
        size = kwargs.pop('size', 0)
        LOG.debug("--Create a volume is %s and size is %d", name, size)
        volume = op_utils.create_volume2(name, size, should_wait=True, **kwargs)
        if volume:
            return self._change_obj_to_dict(volume)
        else:
            return None

    @staticmethod
    def delete(**kwargs):
        """delete a volume"""
        volume_id = kwargs.get('volume').get('id')
        LOG.debug("--Delete volume ID is %s", volume_id)
        return op_utils.delete_volume2(volume_id)

    @staticmethod
    def attach(**kwargs):
        """attach a volume"""
        volume_id = kwargs.get('volume').get('id')
        server_id = kwargs.get('server').get('id')

        LOG.debug("--Attach volume ID=%s from server ID=%s", volume_id, server_id)
        return op_utils.attach_volume(server_id, volume_id)

    @staticmethod
    def detach(**kwargs):
        """attach a volume"""
        volume_id = kwargs.get('volume').get('id')
        server_id = kwargs.get('server').get('id')

        LOG.debug("--Detach volume ID=%s from server ID=%s", volume_id, server_id)
        return op_utils.detach_volume(server_id, volume_id)

    @staticmethod
    def extend(**kwargs):
        """extend a volume"""
        volume_id = kwargs.get('volume').get('id')
        new_size = kwargs.get('size')
        LOG.debug("--Extend volume ID=%s size to =%d", volume_id, new_size)
        return op_utils.extend_volume(volume_id, new_size)

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
