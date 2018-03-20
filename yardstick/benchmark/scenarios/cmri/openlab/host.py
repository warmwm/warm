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


class Host(base.Scenario):
    """Server Operation"""

    __scenario_type__ = "Host"

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

    @staticmethod
    def get_host_list(**kwargs):
        """get host list"""
        available_zone = kwargs.pop("av_zone", None)
        LOG.debug("--Get available zone %s all hosts", available_zone)
        host_list = op_utils.get_host_list(available_zone)

        if host_list:
            #return self._change_obj_to_dict(host_list)
            return host_list
        else:
            return None

    def get_compute_hosts(self, **kwargs):
        """get compute hosts"""
        available_zone = kwargs.get("av_zone", "nova")
        host_num = kwargs.pop("host_num", 1)
        host_list = self.get_host_list(**kwargs)
        my_list = []
        my_list_num = 0
        for host in host_list:
            if host.zone == available_zone:
                my_list.append(self._change_obj_to_dict(host))

            my_list_num = len(my_list)
            if my_list_num >= host_num:
                break

        if my_list_num < host_num:
            LOG.debug("--get_compute_hosts can not get enough hosts, current number is %d", my_list_num)
            return False
        else:
            return my_list

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

        if isinstance(ret_code, list):
            values = ret_code
        else:
            values = [ret_code]

        return self._push_to_outputs(keys, values)
