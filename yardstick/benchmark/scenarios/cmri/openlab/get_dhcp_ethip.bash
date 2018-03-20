#!/bin/bash
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

eth_name=`cat /etc/network/interfaces |grep dhcp |awk '{print $2}'`
value=`ip a |grep $eth_name |grep inet | awk '{print $2}'`
out_put=${value%/*}
echo -e "${out_put}\c"
