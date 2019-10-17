#!/bin/bash
#
#SBATCH --job-name=plotssnet
#SBATCH --output=log_plotssnet
#SBATCH --mem-per-cpu=2000
#SBATCH --time=1:00:00
#SBATCH --array=0

CONTAINER=/cluster/tufts/wongjiradlab/larbys/larbys-containers/singularity_ubdl_deps_py2_10022019.simg
WORKDIR=/cluster/tufts/wongjiradlab/twongj01/dllee-ana/plotssnet
DLLEEDIR=/cluster/tufts/wongjiradlab/twongj01/dev/ubdl

# MCC9 
#TAG=mcc9jan_extbnb
TAG=mcc9_v13_bnbnue_corsika

# SET VARIABLES
SSNETLIST=${WORKDIR}/filelists/${TAG}_ssnet.list
SUPERALIST=${WORKDIR}/filelists/${TAG}_supera.list
OUTDIR=${WORKDIR}/output/${TAG}/

mkdir -p ${OUTDIR}

SETUP="cd ${DLLEEDIR} && source setenv.sh && source configure.sh && cd ${WORKDIR}"

module load singularity
singularity exec ${CONTAINER} bash -c "${SETUP} && ./run_plot_ssnet.sh ${SSNETLIST} ${SUPERALIST} ${OUTDIR} ${TAG}"

