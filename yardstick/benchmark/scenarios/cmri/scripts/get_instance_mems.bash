#!/bin/sh

mem=`free -m|grep Mem|awk '{print $2}'`

echo "${mem}"