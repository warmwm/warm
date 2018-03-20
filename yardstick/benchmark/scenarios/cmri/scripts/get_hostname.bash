#!/bin/sh

hostname=`curl http://169.254.169.254/2009-04-04/meta-data/hostname`

echo "${hostname}"
