#!/bin/sh

##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
echo "n
p
1


w
" | sudo /sbin/fdisk /dev/vdb && /usr/sbin/mkfs.ext4 /dev/vdb1 
sudo mkdir /data1  
sudo mount /dev/vdb1 /data1 
sudo dd if=/dev/zero bs=10M count=1024 of=/data1/data.file  
