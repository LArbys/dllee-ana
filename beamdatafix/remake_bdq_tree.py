import os,sys,json,array
import ROOT as rt

"""
******************************************************************************
*Tree    :bdq       : Beam Data Quality Filter Summary                       *
*Entries :   198594 : Total =        12347168 bytes  File  Size =    6445252 *
*        :          : Tree compression factor =   1.89                       *
******************************************************************************
*Br    0 :run       : run/i                                                  *
*Entries :   198594 : Total  Size=    1051883 bytes  File Size  =     327640 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   3.03     *
*............................................................................*
*Br    1 :subrun    : subrun/i                                               *
*Entries :   198594 : Total  Size=    1060565 bytes  File Size  =     372302 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   2.69     *
*............................................................................*
*Br    2 :sec       : sec/i                                                  *
*Entries :   198594 : Total  Size=    1051883 bytes  File Size  =     659792 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   1.51     *
*............................................................................*
*Br    3 :msec      : msec/i                                                 *
*Entries :   198594 : Total  Size=    1054777 bytes  File Size  =     714674 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   1.39     *
*............................................................................*
*Br    4 :event     : event/i                                                *
*Entries :   198594 : Total  Size=    1057671 bytes  File Size  =     670608 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   1.49     *
*............................................................................*
*Br    5 :tor       : tor/D                                                  *
*Entries :   198594 : Total  Size=    1846267 bytes  File Size  =    1364473 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   1.31     *
*............................................................................*
*Br    6 :horn      : horn/D                                                 *
*Entries :   198594 : Total  Size=    1849161 bytes  File Size  =     677344 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   2.64     *
*............................................................................*
*Br    7 :fom       : fom/D                                                  *
*Entries :   198594 : Total  Size=    1846267 bytes  File Size  =     878971 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   2.03     *
*............................................................................*
*Br    8 :trigger   : trigger/i                                              *
*Entries :   198594 : Total  Size=    1063459 bytes  File Size  =     282758 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   3.56     *
*............................................................................*
*Br    9 :result    : result/O                                               *
*Entries :   198594 : Total  Size=     464777 bytes  File Size  =     275841 *
*Baskets :     2890 : Basket Size=      32000 bytes  Compression=   1.47     *
*............................................................................*
"""
fbdq = rt.TFile("beamdataquality_hist_bnb5e19.root","open")
bdq = fbdq.Get("beamdataquality/bdq")

print "Entries: ",bdq.GetEntries()

fout = rt.TFile("beamdataquality_remix_bnb5e19.root","recreate")
out = rt.TTree("bdq","Beam Quality Data: remixed")

run = array.array('i',[0])
subrun = array.array('i',[0])
event = array.array('i',[0])
sec = array.array('i',[0])
msec = array.array('i',[0])
tor  = array.array('f',[0.0])
horn = array.array('f',[0.0])
fom  = array.array('f',[0.0])
trigger = array.array('i',[0])
result  = array.array('i',[0])

out.Branch( "run", run, "run/I" )
out.Branch( "subrun", subrun, "subrun/I" )
out.Branch( "event", event, "event/I" )
out.Branch( "sec", sec, "sec/I" )
out.Branch( "msec", msec, "msec/I" )
out.Branch( "tor", tor, "tor/F" )
out.Branch( "horn", horn, "horn/F" )
out.Branch( "fom", fom, "fom/F" )
out.Branch( "trigger", trigger, "trigger/I" )
out.Branch( "result", result, "result/I" )

jfile = open("missing_beam_data.json",'r')
jbdq = json.load(jfile)
jfile.close()

bad_entries = {}
nbad = 0
ngood = 0
for ientry in xrange( bdq.GetEntries() ):

    bdq.GetEntry(ientry)

    run[0]     = bdq.run
    subrun[0]  = bdq.subrun
    event[0]   = bdq.event
    sec[0]     = bdq.sec
    msec[0]    = bdq.msec
    tor[0]     = bdq.tor
    horn[0]    = bdq.horn
    fom[0]     = bdq.fom
    trigger[0] = bdq.trigger
    result[0]  = bdq.result
    
    if bdq.fom==-99999:
        # use replacement data
        #print "Replace [",bdq.run,",",bdq.subrun,",",bdq.event,"]"
        srun = "{}".format(bdq.run)
        found = False
        for entrydata in jbdq[srun]:
            if entrydata[1]==bdq.subrun and entrydata[4]==bdq.event:
                found = True
                sec[0]     = entrydata[2]
                msec[0]    = entrydata[3]
                tor[0]     = entrydata[6]
                horn[0]    = entrydata[7]
                fom[0]     = entrydata[8]
                trigger[0] = entrydata[5]

                if horn[0]>172 and horn[0]<176 and fom[0]>0.95 and tor[0]>0.5:
                    result[0] = 1
                else:
                    result[0] = 0
                break
        if not found:
            print "NOT FOUND: [",bdq.run,",",bdq.subrun,",",bdq.event,"]"
            #raw_input()            
        else:
            print "FOUND MISSING: [",bdq.run,",",bdq.subrun,",",bdq.event,"]"

    if result[0]==1:
        ngood += 1
    elif result[0]==0:
        nbad += 1

    out.Fill()

print "numgood: ",ngood
print "numbad:  ",nbad
out.Write()
fout.Close()
