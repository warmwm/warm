#!/bin/bash

# set -e
# set -x
cd $YARDSTICK_REPO_DIR

echo '========================update code from local repo========================'
# git pull lab master

echo '========================update yardstick package========================'
# pip install -U .

# run the ansible yaml
echo '========================run ansible========================'
cd ansible
# source /etc/yardstick/openstack.creds
# ansible-playbook -i inventory.ini $1
ansible-playbook cmri_setup.yaml
ansible-playbook -i inventory.ini cmri_test_5_1_2_10_1.yml  -e network=ext-net
ansible-playbook cmri_teardown.yaml

