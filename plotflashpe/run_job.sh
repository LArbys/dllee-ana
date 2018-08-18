#!/bin/bash

workdir=/cluster/kappa/90-days-archive/wongjiradlab/twongj01/plotflashpe/
workdir_ic=/cluster/kappa/wongjiradlab/twongj01/plotflashpe/

#flist=${workdir}/superalists/mcc8v11_goodtagger_superalist.txt
#flist=${workdir}/superalists/mcc8v6_bnb5e19_goodtagger_superalist.txt
flist=${workdir}/superalists/mcc8v7_bnb_overlay_p01_goodtagger_superalist.txt
CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20180816.img

module load singularity
singularity exec ${CONTAINER} bash -c "source /usr/local/bin/thisroot.sh && cd /usr/local/share/dllee_unified/ && source configure.sh && cd ${workdir_ic} && python run_plotflashpe.py ${flist}"