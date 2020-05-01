#!/bin/bash
#
#SBATCH --job-name=numufilter-nueintrinsics
#SBATCH --output=numufilter-nueintrinsics.txt
#SBATCH --time=120:00
#SBATCH --mem-per-cpu=2000
#SBATCH --array=0-9

source /cluster/tufts/wongjiradlab/twongj01/dllee-ana/run_numu_filter/jobscript_nueintrinsics.sh