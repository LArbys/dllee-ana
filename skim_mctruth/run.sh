#!/bin/bash
#
#SBATCH --job-name=compile_larflow
#SBATCH --output=log_compile_larflow.log
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4000
#SBATCH --time=3-00:00:00
#SBATCH --cpus-per-task=2
#SBATCH --partition batch

INPUT=$1
INPUT_IC=`echo $INPUT | sed 's/90-days-archive//g' | sed 's/tufts/kappa/'`
WORKDIR_IC=/cluster/kappa/wongjiradlab/twongj01/dllee-ana/skim_mctruth/
CONTAINER=/cluster/tufts/wongjiradlab/larbys/images/singularity-larflow/singularity-larflow-v2.img

OUTPUT_IC="test.root"

module load singularity

# clean
#singularity exec --nv ${CONTAINER} bash -c "cd ${LARFLOW_REPO_DIR_INCONTAINER} && source /usr/local/root/release/bin/thisroot.sh && source configure.sh && source clean.sh"

setup="source /usr/local/root/release/bin/thisroot.sh && source /usr/local/larlite/config/setup.sh"
cmd="./mcskim ${INPUT_IC} ${OUTPUT_IC}"

# compile
singularity exec ${CONTAINER} bash -c "cd ${WORKDIR_IC} && ${setup} && ${cmd}"
