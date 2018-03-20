#!/bin/sh

vcpu=`lscpu |grep ^CPU\(s\)|awk '{print $2}'`

echo "${vcpu}"