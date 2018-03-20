#!/bin/sh


`fdisk -l`
`mkfs.ext4 /dev/vdb`
`mount /dev/vdb /mnt`
`touch /mnt/test`
info = `ls /mnt/ | grep "test"`
`umount /dev/vdb`

echo "${info}"

