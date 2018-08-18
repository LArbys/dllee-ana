#!/bin/bash

CONTAINER=/cluster/tufts/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20180816.img
WORKDIR=/cluster/kappa/wongjiradlab/twongj01/plotflashpe/

module load singularity
singularity exec ${CONTAINER} bash -c "source /usr/local/bin/thisroot.sh && cd /usr/local/share/dllee_unified && source configure.sh && cd ${WORKDIR} && make"