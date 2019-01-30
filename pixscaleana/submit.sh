#!/bin/bash
#
#SBATCH --job-name=pixscaleana
#SBATCH --output=log_pixscaleana
#SBATCH --mem-per-cpu=2000
#SBATCH --time=1:00:00
#SBATCH --array=0-19

CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20181010-mcc9beta1.img
WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/twongj01/dllee-ana/pixscaleana/
WORKDIR_IC=/cluster/kappa/wongjiradlab/twongj01/dllee-ana/pixscaleana/

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
#SSNETLIST_IC=${WORKDIR_IC}/mcc8v6_extbnb_ssnet.list
#SUPERALIST_IC=${WORKDIR_IC}/mcc8v6_extbnb_supera.list
#OUTDIR=${WORKDIR}/output/mcc8v6_extbnb/
#OUTDIR_IC=${WORKDIR_IC}/output/mcc8v6_extbnb/

# MCC8v7
TAG=bnbcosmic_detsys_cv

# MCC9 BNB 5e19
#TAG=mcc9tag1_bnb5e19

# MCC9 nue-intrinsic corsika
#TAG=mcc9tag2_nueintrinsic_corsika

SUPERALIST_IC=${WORKDIR_IC}/filelists/flist_supera_${TAG}.list
RECO2DLIST_IC=${WORKDIR_IC}/filelists/flist_reco2d_${TAG}.list
OUTDIR=${WORKDIR}/output/${TAG}/
OUTDIR_IC=${WORKDIR_IC}/output/${TAG}/


mkdir -p ${OUTDIR}

module load singularity

# grid running
singularity exec ${CONTAINER} bash -c "cd ${WORKDIR_IC} && ls && ./run_pixscaleana.sh ${SUPERALIST_IC} ${RECO2DLIST_IC} ${OUTDIR_IC} ${TAG}"

# local running for tests
#singularity exec ${CONTAINER} bash -c "cd ${WORKDIR_IC} && ls && SLURM_ARRAY_TASK_ID=1 ./run_pixscaleana.sh ${SUPERALIST_IC} ${RECO2DLIST_IC} ${OUTDIR_IC} ${TAG}"
