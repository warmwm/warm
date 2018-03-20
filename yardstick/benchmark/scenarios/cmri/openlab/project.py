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
import subprocess

from yardstick.benchmark.scenarios import base
from yardstick.common import constants as consts
import yardstick.common.openstack_utils as op_utils


LOG = logging.getLogger(__name__)


class Project(base.Scenario):
    """Get an OpenStack flavor by name"""

    __scenario_type__ = "Project"

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

    def get_pri_id(self, tenant_name):
        cmd="openstack project show %s |grep 'id' |awk -F '|' '{print $3}'" \
              " |sed -e 's/^[[:space:]]*//'" % tenant_name
        tenant_id = 0
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 cwd=consts.YARDSTICK_REPOS_DIR)
            tenant_id = p.communicate()[0]
        except Exception:
            LOG.info("%s host system failed, caused by %s!", self.action, \
                     p.stderr)
        LOG.info("the teanent id is %s", tenant_id)
        return tenant_id

    def cinder_get_prj_usage(self, **kwargs):
        """create a volume"""
        tenant_name = kwargs.get("tenant_name", None)
        tenant_id = self.get_pri_id(tenant_name)
        LOG.debug("--get project usage, tenant id=%s", tenant_id)
        prj_usage = op_utils.cinder_get_prj_usage(tenant_id, True)
        return prj_usage.gigabytes['in_use']

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
