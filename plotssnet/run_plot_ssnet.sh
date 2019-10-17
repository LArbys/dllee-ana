#!/bin/bash

flist_ssnetout=$1
flist_supera=$2
outdir=$3
tag=$4
arrayid=$SLURM_ARRAY_TASK_ID

jobdir=`printf workdir/%s_job%d ${tag} ${arrayid}`

mkdir -p $jobdir
cd $jobdir

# parse flist 
let start=${arrayid}+1
let end=${arrayid}+3
sed -n ${start},${end}p ${flist_ssnetout} > input_ssnet.txt
sed -n ${start},${end}p ${flist_supera}   > input_supera.txt

outfile=`printf ssnetplots_%s_%03d.root ${tag} ${arrayid}`

./../.././plot_ssnet input_ssnet.txt input_supera.txt $outfile
cp $outfile $outdir/