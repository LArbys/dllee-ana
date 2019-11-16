#!/bin/bash

sample=$1
workdir=$2

cd $workdir

source /usr/local/root/root-6.16.00/bin/thisroot.sh >& /dev/null
cd /cluster/tufts/wongjiradlab/twongj01/production/dllee_unified_opencv3.1_copy2/
source setup.sh >& /dev/null
source configure.sh >& /dev/null
cd $workdir

echo "SLURM ARRAY ID: ${SLURM_ARRAY_TASK_ID}"

jobdir=`printf %s/jobdir_arrayid%03d $sample $SLURM_ARRAY_TASK_ID`
mkdir -p $workdir/$jobdir/
cd $jobdir

# for overlay
python ../../../summary_tree.py -s $sample --jobid $SLURM_ARRAY_TASK_ID --nfiles 50 --ext --ismc

# for ext
#python ../../../summary_tree.py -s $sample --jobid $SLURM_ARRAY_TASK_ID --nfiles 50 --ext

# for bnb
#python ../../../summary_tree.py -s $sample --jobid $SLURM_ARRAY_TASK_ID --nfiles 50

