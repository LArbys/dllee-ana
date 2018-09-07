#!/bin/bash

workdir=/cluster/kappa/90-days-archive/wongjiradlab/twongj01/dllee-ana/plotflashpe/
workdir_ic=/cluster/kappa/wongjiradlab/twongj01/dllee-ana/plotflashpe/

# overlay 
flist=${workdir_ic}/superalists/mcc8v7_bnb_overlay_p00_goodtagger_superalist.txt
#flist=${workdir_ic}/superalists/mcc8v7_bnb_overlay_p01_goodtagger_superalist.txt
taggercfg_ic=/cluster/kappa/wongjiradlab/larbys/pubs/dlleepubs/tagger/tagger_overlay_v2_splity.cfg

# bnb5e19
#flist=${workdir_ic}/superalists/mcc8v6_bnb5e19_goodtagger_superalist.txt
#taggercfg_ic=/cluster/kappa/wongjiradlab/larbys/pubs/dlleepubs/tagger/tagger_data_v2_splity.cfg

# corsika
#flist=${workdir_ic}/superalists/mcc8v11_goodtagger_superalist.txt
#taggercfg_ic=/cluster/kappa/wongjiradlab/larbys/pubs/dlleepubs/tagger/tagger_mc_v2_splity.cfg

# ext

# extunbiased

UNIFIED_IC=/usr/local/share/dllee_unified

CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20180816.img

module load singularity
singularity exec ${CONTAINER} bash -c "source /usr/local/bin/thisroot.sh && cd $UNIFIED_IC && source configure.sh && cd ${workdir_ic} && source run_plotflashpe.sh ${taggercfg_ic} ${flist}"