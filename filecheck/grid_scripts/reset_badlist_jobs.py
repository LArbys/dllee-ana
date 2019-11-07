import os,sys,json

badlist = "badlist.txt"
fbad = open(badlist,'r')
lbad = fbad.readlines()

sample="mcc9jan_extbnb"

rselist = []
for l in lbad:
    l = l.strip()
    run = int(l.split("-")[-2][len("Run"):])
    subrun = int(l.split("-")[-1].split(".")[0][len("SubRun"):])
    print run,subrun,l
    rselist.append( (run,subrun) )

for (run,subrun) in rselist:

    print (run,subrun),": modify DB"

    for table in [sample+"_trackersparsessnet","showerreco_"+sample,"dlmergedsparsessnet_"+sample]:
        print table
        query="UPDATE %s SET status=1 where run=%d and subrun=%d"%( table, run, subrun )
        cmdx="echo \"\\x \\\\\\\\ %s\" | psql -h lnsnudot.mit.edu -U tufts-pubs procdb" %( query )
        pout = os.popen(cmdx)
        plines = pout.readlines()
        for p in plines:
            print p.strip()
