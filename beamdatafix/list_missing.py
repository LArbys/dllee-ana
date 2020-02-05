import os,sys,json

import ROOT as rt

fbdq = rt.TFile("beamdataquality_hist_bnb5e19.root")

bdq = fbdq.Get("beamdataquality/bdq")

print "Entries: ",bdq.GetEntries()

bad_entries = {}
nbad = 0
for ientry in xrange( bdq.GetEntries() ):

    bdq.GetEntry(ientry)

    if bdq.fom<=-99998:
        print "bad entry: ",bdq.run," ",bdq.subrun," ",bdq.event,": ",bdq.fom

        if bdq.run not in bad_entries:
            bad_entries[bdq.run] = []
        
        entry = [ bdq.run, bdq.subrun, bdq.event, bdq.sec, bdq.msec ]
        bad_entries[bdq.run].append( entry )
        nbad += 1

print "bad runs: ",len(bad_entries)
for run in bad_entries:
    bad_entries[run].sort()
print "bad entries: ",nbad

fout = open("bad_bdq_entries.json",'w')
json.dump( bad_entries, fout )
fout.close()
