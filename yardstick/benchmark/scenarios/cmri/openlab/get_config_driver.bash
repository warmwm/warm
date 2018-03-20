#!/bin/bash

##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

mkdir -p /mnt/config
mount /dev/disk/by-label/config-2 /mnt/config > /dev/null 2>&1
cat /mnt/config/openstack/latest/user_data
