#!/bin/bash

inputlist=$1
result_folder=$2
workdir=$3

source /usr/local/root/root-6.16.00/bin/thisroot.sh >& /dev/null
cd /cluster/tufts/wongjiradlab/twongj01/production/dllee_unified_opencv3.1/
source setup.sh >& /dev/null
source configure.sh >& /dev/null
cd $workdir

#echo "SLURM ARRAY ID: ${SLURM_ARRAY_TASK_ID}"

for i in {1..20}
do
    let lineno=20*${SLURM_ARRAY_TASK_ID}+i
    #echo "LOOP $i, LINENO=$lineno"

    supera=$(sed -n ${lineno}p $inputlist | awk '{ print $3 }')
    #echo "supera=$supera"
    if [ -z $supera ]; then
	echo "BREAK empty supera=$supera"
	break;
    fi

    let RUN=$(sed -n ${lineno}p $inputlist | awk '{ print $1 }')
    let SUBRUN=$(sed -n ${lineno}p $inputlist | awk '{ print $2 }')

    #echo "(RUN,SUBRUN): ($RUN,$SUBRUN) $supera"
    tagger=$(echo $supera | sed 's|supera|taggeroutv2-larcv|g')
    ssnetv2=$(echo $supera | sed 's|supera|ssnetserveroutv2-larcv|g')
    #echo "TAGGER: $tagger"
    #echo "SSNET: $ssnetv2"

    outfile=`printf $result_folder/run%d_subrun%d.out $RUN $SUBRUN`
    python /cluster/tufts/wongjiradlab/twongj01/dllee-ana/ssnetcheck/ssnetcheck.py $supera $tagger $ssnetv2 > $outfile

    echo "(RUN,SUBRUN): ($RUN,$SUBRUN) $supera"
    tail -n 1 $outfile
done