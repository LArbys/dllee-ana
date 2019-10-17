#!/bin/bash
#
#SBATCH --job-name=build_plotssnet
#SBATCH --output=log_build_plotssnet
#SBATCH --mem-per-cpu=2000
#SBATCH --time=10:00

CONTAINER=/cluster/tufts/wongjiradlab/larbys/larbys-containers/singularity_ubdl_deps_py2_10022019.simg
WORKDIR=/cluster/tufts/wongjiradlab/twongj01/dllee-ana/plotssnet
DLLEE_DIR=/cluster/tufts/wongjiradlab/twongj01/dev/ubdl/

SETUP="cd $DLLEE_DIR && source setenv.sh && source configure.sh && cd $WORKDIR"
module load singularity
singularity exec ${CONTAINER} bash -c "${SETUP} && make"

