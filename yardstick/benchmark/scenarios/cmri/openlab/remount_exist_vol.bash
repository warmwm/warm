#!/bin/bash

##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
sudo mkdir /data1 > /dev/null 2>&1
sudo mount /dev/vdb1 /data1 > /dev/null 2>&1
sudo md5sum /data1/data.file |awk '{print $1}'