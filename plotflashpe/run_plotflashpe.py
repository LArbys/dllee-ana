import os,sys

arrayid = int(os.environ["SLURM_ARRAY_TASK_ID"])
filesperjob = 1

flist = sys.argv[1]

# change flist to container location
flist = flist.replace("90-days-archive", "")
f = open(flist,'r')
fl = f.readlines()



nstart = arrayid*filesperjob
nend   = (arrayid+1)*filesperjob

for n,l in enumerate(fl[nstart:nend]):
    l = l.strip()
    info = l.split()
    run = int(info[0])
    subrun = int(info[1])
    supera = info[2].replace("90-days-archive","")
    
    taggerlarcv = supera.replace("supera","taggeroutv2-larcv")
    #taggerlarcv = supera.replace("supera","taggerout-larcv")
    #taggerlarcv = supera.replace("supera","ssnetout-larcv") # for version of tagger w/o precuts

    #taggerlarlite = supera.replace("supera","taggerout-larlite")
    taggerlarlite = supera.replace("supera","taggeroutv2-larlite")
    opreco        = supera.replace("supera","opreco")
    #mcinfo        = supera.replace("supera","mcinfo")

    # make run dir
    rundir = "job%d_%d_%d"%(arrayid,run,subrun)
    os.system("mkdir -p %s"%(rundir))
    os.system("cp io.cfg %s/"%(rundir))
    os.system("cp plotflashpe %s/"%(rundir))
    os.system("cd %s"%(rundir))

    flarcv = open("input_larcv.txt",'w')
    print >> flarcv,taggerlarcv
    flarcv.close()

    flarlite = open("input_larlite.txt",'w')
    print >> flarlite,taggerlarlite
    print >> flarlite,opreco
    flarlite.close()

    fout = "../output/out_plotflashpe_%03d_%05d.root"%(run,subrun)

    print "running file %d of %d: rse=(%d,%d), %s"%(n,len(fl),run,subrun,opreco)

    os.system("./plotflashpe %s"%(fout))
    sys.stdout.flush()

f.close()
