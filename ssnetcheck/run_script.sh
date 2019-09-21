#!/bin/bash

inputlist=$1
result_folder=$2
workdir=$3

source /usr/local/root/root-6.16.00/bin/thisroot.sh
cd /cluster/tufts/wongjiradlab/twongj01/production/dllee_unified_opencv3.1/
source setup.sh
source configure.sh
cd $workdir

#SLURM_ARRAY_TASK_ID=200

let lineno=${SLURM_ARRAY_TASK_ID}+1
supera=$(sed -n ${lineno}p $inputlist | awk '{ print $3 }')

let RUN=$(sed -n ${lineno}p $inputlist | awk '{ print $1 }')
let SUBRUN=$(sed -n ${lineno}p $inputlist | awk '{ print $2 }')

echo "(RUN,SUBRUN): ($RUN,$SUBRUN) $supera"

tagger=$(echo $supera | sed 's|supera|taggeroutv2-larcv|g')
ssnetv2=$(echo $supera | sed 's|supera|ssnetserveroutv2-larcv|g')
echo "TAGGER: $tagger"
echo "SSNET: $ssnetv2"

outfile=`printf $result_folder/run%d_subrun%d.out $RUN $SUBRUN`
python /cluster/tufts/wongjiradlab/twongj01/dllee-ana/ssnetcheck/ssnetcheck.py $supera $tagger $ssnetv2 > $outfile

tail -n 2 $outfile
