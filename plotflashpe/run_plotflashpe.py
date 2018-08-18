import os,sys

flist = sys.argv[1]

# change flist to container location
flist = flist.replace("90-days-archive", "")
f = open(flist,'r')
fl = f.readlines()

for n,l in enumerate(fl):
    l = l.strip()
    info = l.split()
    run = int(info[0])
    subrun = int(info[1])
    supera = info[2].replace("90-days-archive","")
    
    taggerlarcv = supera.replace("supera","taggerout-larcv")
    #taggerlarcv = supera.replace("supera","ssnetout-larcv") # for version of tagger w/o precuts

    taggerlarlite = supera.replace("supera","taggerout-larlite")
    opreco        = supera.replace("supera","opreco")
    #mcinfo        = supera.replace("supera","mcinfo")

    flarcv = open("input_larcv.txt",'w')
    print >> flarcv,taggerlarcv
    flarcv.close()

    flarlite = open("input_larlite.txt",'w')
    print >> flarlite,taggerlarlite
    print >> flarlite,opreco
    flarlite.close()

    fout = "output/out_plotflashpe_%03d_%05d.root"%(run,subrun)

    print "running file %d of %d: rse=(%d,%d)"%(n,len(fl),run,subrun)

    os.system("./plotflashpe %s > /dev/null"%(fout))
    sys.stdout.flush()

f.close()
