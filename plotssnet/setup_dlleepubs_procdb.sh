#!/bin/bsh

PUBSDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/pubs

module load python/2.7.6
source ${PUBSDIR}/config/setup.sh
source ${PUBSDIR}/config/personal_conf.sh

export PATH=${PUBSDIR}/dlleepubs/utils/:$PATH
export PYTHONPATH=${PUBSDIR}/dlleepubs/utils:${PYTHONPATH}