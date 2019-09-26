import os,sys

resultdir = os.listdir("resultfiles/")

hasbad = []
brokenfile = []
ifile=0
for f in resultdir:
    run = int(f.split("_")[0][3:])
    subrun = int(f.split("_")[1].split(".")[0][6:])

    p = os.popen("tail -n 1 resultfiles/%s"%(f.strip()))
    if ifile%100==0:
        print "processed file %d of %d"%(ifile,len(resultdir))

    try:
        nbad = int(p.readlines()[-1])
        if nbad>0:
            hasbad.append( (run,subrun,nbad) )
    except:
        brokenfile.append( (run,subrun,1) )

    ifile += 1

hasbad.sort()

f = open('bad_subruns.txt','w')
for (r,s,nbad) in hasbad:
    print "  ",(r,s),": nbad=",nbad
    print>>f,r," ",s
print "HAS BAD: %d of %d"%(len(hasbad),len(resultdir))

print "BROKEN CHECK: ",len(brokenfile)
for (r,s,nbad) in brokenfile:
    print "  ",(r,s),": nbad=",nbad
    print>>f,r," ",s
f.close()
