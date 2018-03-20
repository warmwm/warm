#!/bin/sh

mtu=`cat /sys/class/net/eth0/mtu`

echo "${mtu}"
