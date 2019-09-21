import os,sys

resultdir = os.listdir("resultfiles/")

hasbad = []
for f in resultdir:
    run = int(f.split("_")[0][3:])
    subrun = int(f.split("_")[1].split(".")[0][6:])
    p = os.popen("tail -n 1 resultfiles/%s"%(f.strip()))
    nbad = int(p.readlines()[-1])
    #print "run,subrun: ",run,subrun," nbad=",nbad
    if nbad>0:
        hasbad.append( (run,subrun,nbad) )

print "HAS BAD: %d of %d"%(len(hasbad),len(resultdir))
for (r,s,nbad) in hasbad:
    print "  ",(r,s),": nbad=",nbad

