#!/bin/bash
#
#SBATCH --job-name=plotssnet
#SBATCH --output=log_plotssnet
#SBATCH --mem-per-cpu=2000
#SBATCH --time=1:00:00
#SBATCH --array=0-49

CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20181010-mcc9beta1.img
WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/twongj01/dllee-ana/plotssnet/
WORKDIR_IC=/cluster/kappa/wongjiradlab/twongj01/dllee-ana/plotssnet/

# MCC9EXTBNB BETA1
#SSNETLIST_IC=${WORKDIR_IC}/mcc9_extbnb_beta1_ssnet.list
#SUPERALIST_IC=${WORKDIR_IC}/mcc9_extbnb_beta1_supera.list
#OUTDIR=${WORKDIR}/output/mcc9_extbnb_beta1/
#OUTDIR_IC=${WORKDIR_IC}/output/mcc9_extbnb_beta1/

# MCC8v11 bnb+corsika
#SSNETLIST_IC=${WORKDIR_IC}/mcc8v11_bnbcosmic_detsys_cv_ssnet.list
#SUPERALIST_IC=${WORKDIR_IC}/mcc8v11_bnbcosmic_detsys_cv_supera.list
#OUTDIR=${WORKDIR}/output/mcc8v11_bnbcosmic_detsys_cv/
#OUTDIR_IC=${WORKDIR_IC}/output/mcc8v11_bnbcosmic_detsys_cv/

# MCC8v6 EXTBNB
SSNETLIST_IC=${WORKDIR_IC}/mcc8v6_extbnb_ssnet.list
SUPERALIST_IC=${WORKDIR_IC}/mcc8v6_extbnb_supera.list
OUTDIR=${WORKDIR}/output/mcc8v6_extbnb/
OUTDIR_IC=${WORKDIR_IC}/output/mcc8v6_extbnb/

mkdir -p ${OUTDIR}

module load singularity
singularity exec ${CONTAINER} bash -c "cd ${WORKDIR_IC} && ls && ./run_plot_ssnet.sh ${SSNETLIST_IC} ${SUPERALIST_IC} ${OUTDIR_IC}"
