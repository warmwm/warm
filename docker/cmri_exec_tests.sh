#!/bin/bash

source /etc/yardstick/openstack.creds

# set -e
# set -x
cd $YARDSTICK_REPO_DIR

# echo '========================update code from local repo========================'
# git pull lab master

# echo '========================update yardstick package========================'
# pip install -U .

# run the suite yaml
echo '========================run yaml file========================'
result=$(echo $1 | grep "test_suites")
if [[ "$result" != "" ]]; then
    yardstick task start --suite tests/opnfv/$1
else
    yardstick task start tests/opnfv/$1
fi

