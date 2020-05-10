import os,sys,array
import ROOT as rt

"""
make weight tree that picks out best vertex in an event
"""

#finputname = "mcc9_v29e_dl_run3_G1_bnb_dlfilter_1e1p_lowBDT_partial_fvv.root"
#finputname = "../../datafiles/ntuples_v28-40_forNeutrino2020/mcc9_v29e_dl_run3_G1_bnb_dlana_open1e19_fvv.root"
finputname = sys.argv[1]

finput = rt.TFile(finputname)
fvv = finput.Get("dlana/FinalVertexVariables")

nentries = fvv.GetEntries()

foutname = finputname.replace(".root","_multivtx.root")
fout = rt.TFile(foutname,"new")
tweight = rt.TTree("multivtxtree","Duplicate Vertex weight and cut tree")

run    = array.array('i',[0])
subrun = array.array('i',[0])
event  = array.array('i',[0])
vtxid  = array.array('i',[0])
evweight = array.array('f',[0.0])
evscore  = array.array('f',[0.0])
keepvtx  = array.array('i',[0])
tweight.Branch("run",run,"run/I")
tweight.Branch("subrun",subrun,"subrun/I")
tweight.Branch("event",event,"event/I")
tweight.Branch("vtxid",vtxid,"vtxid/I")
tweight.Branch("evweight",evweight,"evweight/F")
tweight.Branch("evscore", evscore, "evscore/F")
tweight.Branch("keepvtx", keepvtx, "keepvtx/I")

rse_scores = {}

print "Loop to define max RSE score"
for ientry in xrange(nentries):
    fvv.GetEntry(ientry)
    if ientry%10000==0:
        print " entry ",ientry
    rse = (fvv.run,fvv.subrun,fvv.event)
    if rse not in rse_scores:
        rse_scores[rse] = fvv.BDTscore_1e1p
    elif fvv.BDTscore_1e1p>rse_scores[rse]:
        rse_scores[rse] = fvv.BDTscore_1e1p
            

rsev_dict = {}
print "Loop to define weight"
rse_filled = {}
for ientry in xrange(nentries):

    if ientry%10000==0:
        print " entry ",ientry
    
    fvv.GetEntry(ientry)
    run[0]    = fvv.run
    subrun[0] = fvv.subrun
    event[0]  = fvv.event
    vtxid[0]  = fvv.vtxid
    rse  = (fvv.run,fvv.subrun,fvv.event)
    rsev = (fvv.run,fvv.subrun,fvv.event,fvv.vtxid)
    if rse not in rse_filled and fvv.BDTscore_1e1p>=rse_scores[rse]:
        evweight[0] = 1.0
        keepvtx[0]  = 1        
        rse_filled[rse] = True
    else:
        keepvtx[0] = 0
        evweight[0] = 0.0
    evscore[0] = fvv.BDTscore_1e1p

    if rsev not in rsev_dict:
        rsev_dict[rsev] = True
    else:
        print "repeated RSEV! ",rsev
        keepvtx[0] = 0
    
    tweight.Fill()

tweight.Write()
fout.Close()

print "made: ",foutname
            
        
        
