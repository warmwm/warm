##############################################################################
# Copyright (c) 2017 CMRI
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

LOG = logging.getLogger(__name__)


class GetKeyPair(base.Scenario):
    """Get Keypair:key_path from instance build by Context:Heat"""

    __scenario_type__ = "GetKeyPair"

    def __init__(self, scenario_cfg, context_cfg):
        self.scenario_cfg = scenario_cfg
        self.context_cfg = context_cfg
        self.options = self.scenario_cfg.get('options', {})
        
        host = self.context_cfg['host']
        self.key_filename = host.get('key_filename', '/root/.ssh/id_rsa')
        
    def run(self, result):
        keys = self.scenario_cfg.get('output', '').split()
        values = [self.key_filename]
        return self._push_to_outputs(keys, values)

