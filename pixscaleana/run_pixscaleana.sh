#!/bin/bash

# note, we are inside the container

flist_supera=$1
flist_reco2d=$2
outdir=$3
tag=$4
arrayid=$SLURM_ARRAY_TASK_ID

jobdir=`printf jobdirs/job%d ${arrayid}`

# parse flist 
let line=${arrayid}+1
superafile=`sed -n ${line}p ${flist_supera} | sed 's/90-days-archive//g'`
reco2dfile=`sed -n ${line}p ${flist_reco2d} | sed 's/90-days-archive//g'`

workdir=$PWD

source /usr/local/bin/thisroot.sh

# DLLEE UNIFIED REPO TO USE

# inside container
cd /usr/local/share/dllee_unified

# local tufts build
#cd /cluster/kappa/wongjiradlab/twongj01/dllee_unified/

source configure.sh

export PATH=${LARLITECV_BASEDIR}/app/AnalyzeTagger:${PATH}

cd $workdir

mkdir -p $jobdir
cd $jobdir/

outfile=`printf out_pixscaleana_%s_%03d.root ${tag} ${arrayid}`
#python plot_ssnet.py $ssnetfile $superafile out_plotssnet_mcc9_extbnb_beta1_${arrayid}.root > log_job${arrayid}.txt || exit
#./plot_ssnet $ssnetfile $superafile out_plotssnet_mcc9_extbnb_beta1_${arrayid}.root > log_job${arrayid}.txt || exit
run_pixelscale_analysis $superafile $reco2dfile ${outfile} mcc8 >& log_job${arrayid}.txt || exit
 
# finally copy output
mv ${outfile} $outdir/

# clean up
cd $workdir
rm -r $jobdir