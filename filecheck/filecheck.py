import os,sys, array

import ROOT as rt
from larlite import larlite

dataset = "mcc9_v13_nueintrinsics_overlay_run1"
filelist = open("filelists/%s_mcinfo.list"%(dataset),'r')

lfilelist = filelist.readlines()
print "Number of files in filelist: ",len(lfilelist)

out = rt.TFile("output_filecheck_plots_%s.root"%(dataset),"recreate")

ttree = rt.TTree("filecheck","MC File statistics")

# vars
idx = array.array('i',[0])
run = array.array('i',[0])
subrun = array.array('i',[0])
nentries = array.array('i',[0])
pot = array.array('f',[0.0])

ttree.Branch("idx",idx,"idx/I")
ttree.Branch("run",run,"run/I")
ttree.Branch("subrun",subrun,"subrun/I")
ttree.Branch("nentries",nentries,"nentries/I")
ttree.Branch("pot",pot,"pot/F")

idx[0] = 0
for f in lfilelist:
    if ".root" not in f or "mcinfo" not in f:
        continue
    print "ana: ",f.strip()
    fin = rt.TFile( f.strip() )
    pot_table  = fin.Get("potsummary_generator_tree")
    larlite_id = fin.Get("larlite_id_tree")
    larlite_id.GetEntry(0)
    run[0] = larlite_id._run_id
    subrun[0] = larlite_id._subrun_id

    nentries[0] = larlite_id.GetEntries()
    pot[0] = 0.0
    for i in range(pot_table.GetEntries()):
        bytes = pot_table.GetEntry(i)
        if bytes>0:
            #print pot_table.potsummary_generator_branch.totpot,type(pot_table.totpot),type(pot[0])
            pot[0] += pot_table.potsummary_generator_branch.totpot

    ttree.Fill()
    fin.Close()
    idx[0] += 1
    
print "WRITE"
out.Write()
print "DONE"
