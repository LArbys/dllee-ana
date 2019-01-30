#!/bin/bash

CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20181010-mcc9beta1.img
WORKDIR_IC=/cluster/kappa/wongjiradlab/twongj01/dllee-ana/plotssnet/

module load singularity
singularity exec ${CONTAINER} bash -c "cd ${WORKDIR_IC} && source setup_container.sh ${WORKDIR_IC} && make clean && make"