#!/bin/bash

workdir=$PWD

# setup root
source /usr/local/root/release/bin/thisroot.sh
cd /usr/local/larlite
source config/setup.sh

cd $workdir
make

echo "FIN"