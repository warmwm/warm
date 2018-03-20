#!/bin/sh

volume_num=`sudo fdisk -l|grep ^'Disk /dev/[vs]'|wc -l`

echo "${volume_num}"