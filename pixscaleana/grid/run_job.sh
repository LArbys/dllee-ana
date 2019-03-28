#!/bin/bash

# we assume this is being called from within a container

# configuration
pixanadir=/cluster/kappa/90-days-archive/wongjiradlab/twongj01/dllee-ana/pixscaleana/grid
superalist=${pixanadir}/../filelists/flist_supera_mcc8v11_bnbcosmic_detsys_cv.list
rerunlist=${pixanadir}/rerun_processing.list

# set up environment
cd /cluster/kappa/90-days-archive/wongjiradlab/twongj01/ubdl
source setenv.sh
source configure.sh

# get the jobid and input file
# get the filepath
let lineno=${SLURM_ARRAY_TASK_ID}+1
jobid=`sed -n ${lineno}p ${rerunlist} | awk '{ print $1 }'`
larcvpath=`sed -n ${lineno}p ${rerunlist} | awk '{print $2 }'`
echo "JOBID: ${jobid}"
echo "LARCV INPUT: ${larcvpath}"

# get reco2d filename. can build from supera name typically
reco2dfile=`echo ${larcvpath} | sed 's/supera/reco2d/'`
echo "reco2dfile: ",$reco2dfile

# extract the filename
larcvfilename=$(basename -- $larcvpath)
echo $larcvfilename

# create the output file name
pixanafilename=`echo ${larcvfilename} | sed 's/supera/pixscaleana/'`
echo $pixanafilename

# prep the work directory
workdir=`printf ${pixanadir}/workdir/jobid%04d ${jobid}`
echo $workdir
mkdir -p $workdir


cd ${workdir}
echo "./../../../run_pixscale_ana ${larcvpath} ${reco2dfile} ${pixanafilename}"
./../../../run_pixscale_ana ${larcvpath} ${reco2dfile} ${pixanafilename} >& log
