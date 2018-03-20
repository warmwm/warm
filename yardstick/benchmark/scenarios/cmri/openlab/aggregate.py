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


class Aggregate(base.Scenario):
    """Server Operation"""

    __scenario_type__ = "Aggregate"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg

        self.action = getattr(self, self.scenario_cfg['action'])
        self.options = self.scenario_cfg['options']

        self.setup_done = False

    def setup(self):
        """scenario setup"""
        pass

    def create_aggregate(self, **kwargs):
        """create a aggregate"""
        name = kwargs.pop("name", None)
        available_zone = kwargs.pop("av_zone", None)
        LOG.debug("--Create a host aggregate is %s in avaiable zone %s", name, available_zone)
        aggregate = op_utils.create_aggregate(name, available_zone)

        if aggregate:
            return self._change_obj_to_dict(aggregate)
        else:
            return False

    @staticmethod
    def create_aggregate_with_host(**kwargs):
        """create a aggregate"""
        name = kwargs.pop("name", None)
        available_zone = kwargs.pop("av_zone", None)
        host_name = kwargs.pop("host").pop("host", None)
        LOG.debug("--Create a host aggregate is %s in avaiable zone %s with host %s", name, \
                  available_zone, host_name)
        aggregate = op_utils.create_aggregate(name, available_zone)
        return op_utils.add_host_to_aggregate(aggregate['id'], host_name)

    @staticmethod
    def update_aggregate_av_zone(**kwargs):
        """scenario setup"""
        aggregate = kwargs.get("aggregate")
        aggregate_id = aggregate.get("id")
        values = {"availability_zone": kwargs.get("av_zone")}
        return op_utils.update_aggregate_av_zone(aggregate_id, values)

    @staticmethod
    def delete_aggregate(**kwargs):
        """scenario setup"""
        aggregate = kwargs.pop("aggregate", None)
        aggregate_id = aggregate.get("id", None)
        return op_utils.delete_aggregate(aggregate_id)

    @staticmethod
    def add_host_to_aggregate(**kwargs):
        """scenario setup"""
        aggregate = kwargs.get("aggregate", None)
        aggregate_id = aggregate.get("id", None)
        #host = kwargs.get("host", None)
        #host_name = host.host_name
        host_name = kwargs.get("host").get("host", None)
        return op_utils.add_host_to_aggregate(aggregate_id, host_name)

    @staticmethod
    def remove_host_from_aggregate(**kwargs):
        """scenario setup"""
        aggregate = kwargs.pop("aggregate", None)
        aggregate_id = aggregate.get("id", None)
        host_name = kwargs.get("host").get("host", None)
        #host_name = host.host_name
        return op_utils.remove_hosts_from_aggregate(aggregate_id, host_name)

    @staticmethod
    def remove_hosts_from_aggregate(**kwargs):
        """scenario setup"""
        aggregate = kwargs.pop("aggregate", None)
        aggregate_id = aggregate.get("id", None)
        return op_utils.remove_hosts_from_aggregate(aggregate_id)

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
