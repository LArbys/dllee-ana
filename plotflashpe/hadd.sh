#!/bin/bash
#
#SBATCH --job-name=hadd_plotflashpe
#SBATCH --output=log_hadd_plotflashpe.log
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2000
#SBATCH --time=10:00

OUTPUT=out_plotflashpe_mcc8v7_bnb_overlay_p00_test.root
CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20180816.img
WORKDIR_IC=/cluster/kappa/wongjiradlab/twongj01/dllee-ana/plotflashpe

module load singularity
singularity exec ${CONTAINER} bash -c "source /usr/local/bin/thisroot.sh && cd /tmp/ && hadd -f ${OUTPUT} ${WORKDIR_IC}/output/*.root && cp ${OUTPUT} ${WORKDIR_IC}/"
