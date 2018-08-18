#!/bin/bash
#
#SBATCH --job-name=plotflashpe
#SBATCH --output=log_plotflashpe.log
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2000
#SBATCH --time=3-00:00:00

cd /cluster/kappa/90-days-archive/wongjiradlab/twongj01/plotflashpe && source run_job.sh