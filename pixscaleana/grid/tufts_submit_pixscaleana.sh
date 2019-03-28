#!/bin/bash

# slurm submission script to build ubdl

#SBATCH --job-name=pixscaleana
#SBATCH --output=log_pixscaleana.log
#SBATCH --mem-per-cpu=2000
#SBATCH --time=10:00
#SBATCH --array=0-500

container=/cluster/tufts/wongjiradlab/larbys/larbys-containers/ubdl_singularity_031219.img

# get dir where we called script
workdir=/cluster/kappa/90-days-archive/wongjiradlab/twongj01/dllee-ana/pixscaleana/grid

module load singularity
singularity exec ${container} bash -c "cd ${workdir} && source run_job.sh"

