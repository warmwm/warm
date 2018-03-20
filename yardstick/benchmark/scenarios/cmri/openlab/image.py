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


class Image(base.Scenario):
    """Get an OpenStack flavor by name"""

    __scenario_type__ = "Image"

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
        """create an image"""
        '''
        flavor_name = kwargs.pop("name", "yardstick_test_flavor")
        ram = kwargs.pop('ram', 0)
        vcpus = kwargs.pop('vcpus', 0)
        disk = kwargs.pop('disk', 0)
        kwargs.pop('flavor', None)
        LOG.debug("--Create a flavor is %s", flavor_name)
        flavor = op_utils.create_flavor(flavor_name, ram,  \
                   vcpus, disk, **kwargs)

        if flavor:
            return self._change_obj_to_dict(flavor)
        else:
            return False
        '''
        pass

    @staticmethod
    def delete(**kwargs):
        """delete a flavor"""
        '''
        flavor = kwargs.get('flavor', None)
        LOG.debug("--Delete flavor ID is %s", flavor['id'])
        return op_utils.delete_flavor(flavor['id'])
        '''
        pass

    def get_image_by_name(self, **kwargs):
        image_name = kwargs.get('name')
        image = op_utils.get_image_by_name2(image_name)
        if image:
            return self._change_obj_to_dict(image)
        else:
            return None

    @staticmethod
    def get_image_id_by_name(**kwargs):
        image_name = kwargs.get('name')
        image = op_utils.get_image_by_name2(image_name)
        if image:
            return image.get('id')
        else:
            return None

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
