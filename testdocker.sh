#!/bin/bash
set -x

volumename=$1
indockercmd='cd /recastbase/ && ../recast_cap/testrunbackend.py rootflow.yml http://physics.nyu.edu/~lh1132/dummycomplex.zip fit.workspace.root,nonexistent,world.txt --no-cleanup'
indockercmdesc="''"$indockercmd"''"
echo "$indockercmdesc"
docker volume create --name $volumename
docker run -it -e RECAST_CAP_TOPLVL=from-github/testing/busybox-flow  \
               -v /var/run/docker.sock:/var/run/docker.sock \
               -v $volumename:/recastbase \
               --rm \
	       -e RECAST_IN_DOCKER_WORKDIRS_VOL=$(docker volume inspect -f '{{.Mountpoint}}' $volumename) \
               lukasheinrich/recast-cap-demo bash -c "$indockercmdesc"
