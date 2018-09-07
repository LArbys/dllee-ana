#!/bin/bash

workdir=$1
flist=$2
arrayid=$SLURM_ARRAY_TASK_ID
let filesperjob=5

# make jobdir
jobdir=`printf job%d ${arrayid}`
mkdir $jobdir

# copy cfg and binary
cp plotflashpe $jobdir/
cp io.cfg $jobdir/

# go to jobdir
cd $jobdir

# parse flist
((nstart = filesperjob*arrayid+1))
echo $nstart
(( nend=filesperjob*(arrayid+1) ))
echo $nend
((nquit=nend+1))

# larcv files
sed -n ${nstart},${nend}p $flist | awk '{print $3 }' | sed s/supera/taggeroutv2-larcv/ | sed s/90-days-archive// > input_larcv.txt

# larlite files
sed -n ${nstart},${nend}p $flist | awk '{print $3 }' | sed s/supera/opreco/ | sed s/90-days-archive// > input_larlite.txt
sed -n ${nstart},${nend}p $flist | awk '{print $3 }' | sed s/supera/taggeroutv2-larlite/ | sed s/90-days-archive// >> input_larlite.txt

fout=`printf ../output/out_plotflashpe_%04d.root $arrayid`
./plotflashpe $fout > /dev/null || exit

cd ../
rm -r $jobdir