#!/usr/bin/env python
import os,sys


# use python for better sting manip
#if len(sys.argv)==3:
#    inputpath = sys.argv[1]
#    outputdir = sys.argv[2]
#el
if len(sys.argv)==3:
    jobid = int(os.environ["SLURM_ARRAY_TASK_ID"])
    inputlist  = sys.argv[1]
    outputdir  = sys.argv[2]
else:
    print "error"
    sys.exit(-1)

f = open(inputlist,'r')
inputpath = f.readlines()[jobid].strip()
fname = os.path.basename( inputpath )
#runnum = int(fname.split("-")[1].split("Run")[-1])
#subrun = int(fname.split("-")[2].split("SubRun")[-1].split(".")[0])
fout = fname.replace("reco2d","mcskim").replace("mcinfo","mcskim")
outputpath = "%s/%s"%(outputdir,fout)

outputdir_ic  = outputdir.replace("90-days-archive",'')
outputpath_ic = outputpath.replace("90-days-archive",'')
inputpath_ic  = inputpath.replace("90-days-archive",'')

if os.path.exists( outputpath_ic ) and not rerun:
    print "File exists, do not rerun"
    sys.exit(0)

cmd = "mkdir -p %s && ./mcskim %s %s"%(outputdir_ic,inputpath_ic,outputpath_ic)
print cmd
os.system(cmd)
