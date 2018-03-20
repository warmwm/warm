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



class CreateProject(base.Scenario):
    """Create a project"""

    __scenario_type__ = "CreateProject"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg['options']

        self.project_names = self.options.get('project_names', None)

        self.setup_done = False

    def setup(self):
        """scenario setup"""

        self.setup_done = True

    def run(self, result):
        """execute the test"""

        if not self.setup_done:
            self.setup()

        for project in self.project_names:
            LOG.info("Creating project '%s'", project)

            cmd_create = "openstack project create %s" % (project)

            try:
                p = subprocess.Popen(cmd_create, shell=True, stdout=subprocess.PIPE)
                print(p.communicate()[0])

            except Exception:
                result.update({"Create User": 0})
                LOG.info("Create project failed!")
                raise  RuntimeError("Create project failed!")

        result.update({"Create Project": 1})
        LOG.info("Create Project successful!")
        values = ['0']

        for project in self.project_names:
            cmd = "openstack project show -f json %s" % (project)

            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                project_json = json.loads(p.communicate()[0])
            except Exception:
                raise RuntimeError("Get project_id failed!")

            values.append(project_json['id'])

        keys = self.scenario_cfg.get('output', '').split()

        return self._push_to_outputs(keys, values)
