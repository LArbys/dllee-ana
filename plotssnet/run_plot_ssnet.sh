#!/bin/bash

flist_ssnetout=$1
flist_supera=$2
outdir=$3
tag=$4
arrayid=$SLURM_ARRAY_TASK_ID

jobdir=`printf job%d ${arrayid}`

# parse flist 
let line=${arrayid}+1
ssnetfile=`sed -n ${line}p ${flist_ssnetout} | sed 's/90-days-archive//g'`
superafile=`sed -n ${line}p ${flist_supera} | sed 's/90-days-archive//g'`

echo $ssnetfile
echo $superafile

workdir=$PWD

source /usr/local/bin/thisroot.sh
cd /usr/local/share/dllee_unified
source configure.sh

cd $workdir

mkdir $jobdir
cp plot_ssnet.py $jobdir/
cp plot_ssnet $jobdir/

cd $jobdir

outfile=`printf out_plotssnet_%s_%02d.root ${tag} ${arrayid}`
#python plot_ssnet.py $ssnetfile $superafile out_plotssnet_mcc9_extbnb_beta1_${arrayid}.root > log_job${arrayid}.txt || exit
#./plot_ssnet $ssnetfile $superafile out_plotssnet_mcc9_extbnb_beta1_${arrayid}.root > log_job${arrayid}.txt || exit
./plot_ssnet $ssnetfile $superafile  ${outfile} >& log_job${arrayid}.txt || exit
 
# finally copy output
mv ${outfile} $outdir/

# clean up
cd ..
rm -r $jobdir





