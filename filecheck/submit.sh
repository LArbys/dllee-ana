#!/bin/bash

#SBATCH --job-name=filecheck
#SBATCH --output=filecheck.log
#SBATCH --mem-per-cpu=2000
#SBATCH --time=1:00:00

cd /cluster/tufts/wongjiradlab/twongj01/dllee-ana/filecheck && source run.sh