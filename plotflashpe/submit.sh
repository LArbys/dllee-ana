#!/bin/bash
#
#SBATCH --job-name=plotflashpe
#SBATCH --output=log_plotflashpe.log
#SBATCH --mem-per-cpu=2000
#SBATCH --time=3-00:00:00
#SBATCH --array=0-49

cd /cluster/kappa/90-days-archive/wongjiradlab/twongj01/dllee-ana/plotflashpe && source run_job.sh