#!/bin/sh
rm -rf workdirs
mkdir -p workdirs/jobguid/inputs
(cd workdirs/jobguid/inputs && curl -O http://physics.nyu.edu/~lh1132/michal.zip && unzip michal.zip)
./testrun.py pheno_workflows/madgraph_delphes.yml jobguid
