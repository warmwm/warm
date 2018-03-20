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
import os
import tempfile

from yardstick.benchmark.scenarios import base
from yardstick.common.ansible_common import AnsibleCommon
from yardstick.common import constants as consts

LOG = logging.getLogger(__name__)


class AnsiblePlaybook(base.Scenario):
    """Execute ansible playbook"""

    __scenario_type__ = "AnsiblePlaybook"

    def __init__(self, scenario_cfg, context_cfg):
        options = scenario_cfg['options']

        self.playbook = options.get('playbook')
        if not self.playbook:
            raise RuntimeError('Playbook must be provided')
        self.playbook = os.path.join(consts.ANSIBLE_DIR, self.playbook)

        self.extra_vars = options.get('extra_vars', {})

        self.executor = AnsibleCommon(nodes=context_cfg.get('pod_info', []))
        self.executor.gen_inventory_ini_dict()

    def run(self, result):
        """execute the test"""

        tmpdir = tempfile.mkdtemp(prefix='ansible-')
        self.executor.execute_ansible(self.playbook, tmpdir,
                                      extra_vars=self.extra_vars)

