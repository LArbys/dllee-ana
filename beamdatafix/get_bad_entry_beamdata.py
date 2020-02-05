import os,sys,json
import ROOT as rt

beamdata_dir = "/pnfs/uboone/persistent/uboonebeam/beam_data/bnb_data/"

fin = open("bad_bdq_entries.json",'r')

jbad = json.load(fin)

runs = jbad.keys()
runs.sort()

missing_data = {}
nbad = 0
ngood = 0

for run in runs:

    run = int(run)

    if run not in missing_data:
        missing_data[run] = []

    rundir = "%02d/%02d/%02d/%02d"%( run/1000000, run/10000, run/100, run%100 )
    beamfile = "beamdata_%08d.root"%(run)

    beampath = beamdata_dir + "/" + rundir + "/" + beamfile
    print "RUN ",run,": ",beampath

    bad_entries = jbad["%d"%(run)]

    tfile = rt.TFile( beampath )
    tbnb = tfile.Get("bnb")

    print "  bad entries: ",len(bad_entries)
    print "  bnb entries: ",tbnb.GetEntries()

    ientry = 0
    for bad_entry in bad_entries:
        print "FIND ",bad_entry
        if ientry>0:
            ientry -= 1
        if ientry<0:
            ientry = 0
        byte = tbnb.GetEntry(ientry)
        found = False
        bestdiff = -1.0
        bestindex = 0
        last_subrun = -1
        last_subrun_idx = 0
        while byte>0 and not found:

            # check match with seconds
            msec = (tbnb.tstamp+40)%1000
            sec  = (tbnb.tstamp+40)/1000

            msecdiff = (bad_entry[3]-sec)*1000.0 + (bad_entry[4]-msec)
            if abs(msecdiff) < bestdiff or bestdiff<0:
                bestdiff = abs(msecdiff)
                bestindex = ientry

            #if tbnb.subrun==bad_entry[1] and abs(msecdiff)<100:
            #    print "    ",tbnb.tstamp," ",sec," ",msec," diff=",msecdiff
            #    found = True
            if tbnb.subrun>bad_entry[1]:
                break

            if tbnb.subrun!=last_subrun:
                last_subrun_idx = ientry
                last_subrun = tbnb.subrun

            ientry += 1
            byte = tbnb.GetEntry(ientry)


        tbnb.GetEntry(bestindex)
        msec = (tbnb.tstamp+40)%1000
        sec  = (tbnb.tstamp+40)/1000
        data = [ tbnb.run, tbnb.subrun, sec, msec, bad_entry[2], tbnb.e1dcnt, tbnb.tor860, tbnb.thcurr, tbnb.fom2, bestdiff ]

        if bestdiff<100:
            ngood += 1
        else:
            nbad += 1
            #raise RuntimeError("could not find entry!! best diff {} msec".format(bestdiff))

        print "  SET : best diff {} msec, ngood={} nbad={} ".format(bestdiff,ngood,nbad),data
        ientry = last_subrun_idx-1
        missing_data[run].append( data )

print "ngood matches: ",ngood
print "nbad matches: ",nbad

fout = open("missing_beam_data.json",'w')
json.dump( missing_data, fout )
fout.close()
            


