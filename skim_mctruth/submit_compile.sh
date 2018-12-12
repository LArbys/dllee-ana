#!/bin/bash
#
#SBATCH --job-name=compile_larflow
#SBATCH --output=log_compile_larflow.log
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4000
#SBATCH --time=3-00:00:00
#SBATCH --cpus-per-task=2
#SBATCH --partition batch

WORKDIR_IC=/cluster/kappa/wongjiradlab/twongj01/dllee-ana/skim_mctruth/
CONTAINER=/cluster/tufts/wongjiradlab/larbys/images/singularity-larflow/singularity-larflow-v2.img

module load singularity

# clean
#singularity exec --nv ${CONTAINER} bash -c "cd ${LARFLOW_REPO_DIR_INCONTAINER} && source /usr/local/root/release/bin/thisroot.sh && source configure.sh && source clean.sh"

# compile
singularity exec ${CONTAINER} bash -c "cd ${WORKDIR_IC} && source compile.sh"
