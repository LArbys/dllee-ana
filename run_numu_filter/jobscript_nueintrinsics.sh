#!/bin/bash

#SAMPLE
SAMPLE=mcc9_v13_nueintrinsics_overlay_run1

# ANA DIR
ANA_DIR=/cluster/tufts/wongjiradlab/twongj01/dllee-ana/run_numu_filter

# where the selection scripts live
DLLEE_DIR=/cluster/tufts/wongjiradlab/twongj01/production/dllee_unified_opencv3.1_copy2

# files to run
FILELIST=$ANA_DIR/filelists/dlreco_mcc9_v13_nueintrinsics_overlay_run1.txt

# files to run per job
NFILES=1
CONTAINER=/cluster/tufts/wongjiradlab/larbys/larbys-containers/singularity_ubdl_deps_py2_10022019.simg

# final output dir
FINAL_OUT_DIR=$ANA_DIR/out_$SAMPLE/
mkdir -p $FINAL_OUT_DIR

# for debug (slurm will set this up for us automatically if we use the array argument)
#SLURM_ARRAY_TASK_ID=10

# define start and end lines in filelist to run
let start=$NFILES*$SLURM_ARRAY_TASK_ID+1
let end=$NFILES*${SLURM_ARRAY_TASK_ID}+$NFILES

# working directory
workdir=/tmp

# need to have unique job directory so jobs dont collide
jobdir=$workdir/numu_filter_$SAMPLE_$SLURM_ARRAY_TASK_ID
mkdir -p $jobdir
cd $jobdir

# get list of files
sed -n ${start},${end}p $FILELIST > runlist.txt

# define parameters for running script
outdir=$jobdir/out
#calibmap=/cluster/tufts/wongjiradlab/twongj01/1L1PSelection/CalibrationMaps_MCC9.root
#showerreco=/cluster/tufts/wongjiradlab/twongj01/1L1PSelection/SSNetShowerRecoOut_nueintrinsics.txt

# make output directory
mkdir -p $outdir

# SETUP COMMANDS for container
JOB_SETUP="export PYTHONPATH=${ANA_DIR}:$PYTHONPATH && cd ${DLLEE_DIR} && source setup_tufts_container.sh && source configure.sh && export PATH=${DLLEE_DIR}/larlitecv/app/dllee/bin:${PATH} && cd $jobdir"

# loop over files to run
for f in `cat runlist.txt`
do
    dlreco=$f;
    COMMAND="python ${ANA_DIR}/run_numu_filter.py -i ${dlreco} -s ${SAMPLE} -t overlay -od ${outdir} >& /dev/null"
    echo $COMMAND
    singularity exec $CONTAINER bash -c "$JOB_SETUP && $COMMAND"
done

cp $outdir/merged*.root $FINAL_OUT_DIR/

echo "FIN"