import os,sys,array,pickle
import ROOT as rt

"""
make weight tree that picks out best vertex in an event
"""

selection="1e1p"

#finputname = "mcc9_v29e_dl_run3_G1_bnb_dlfilter_1e1p_lowBDT_partial_fvv.root"
#finputname = "../../datafiles/ntuples_v28-40_forNeutrino2020/mcc9_v29e_dl_run3_G1_bnb_dlana_open1e19_fvv.root"
finputname = sys.argv[1]

finput = rt.TFile(finputname)
fvv = finput.Get("dlana/FinalVertexVariables")

with open("GoodRuns_Run1-Run4_5-8-20.pickle",'r') as f:
    goodrunlist = pickle.load(f)

print "runs in good run list: ",len(goodrunlist),type(goodrunlist)
ntrue = 0
nfalse = 0
for k,v in goodrunlist.items():
    if v:
        ntrue +=1
    else:
        nfalse += 1
print ntrue," ",nfalse

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
rse_maxvtxid = {}

print "Loop to define max RSE score"
for ientry in xrange(nentries):
    fvv.GetEntry(ientry)
    if ientry%10000==0:
        print " entry ",ientry
    rse = (fvv.run,fvv.subrun,fvv.event)
    if rse not in rse_scores:
        # put in some default score
        rse_scores[rse] = -1
        rse_maxvtxid[rse] = -1

    # valid scores are only if other cuts pass
    if selection=="1e1p":
        if ( fvv.PassSimpleCuts==1 and
             fvv.PassPMTPrecut==1 and
             fvv.MaxShrFrac>0.2 and
             fvv.Proton_Edep>60.0 and
             fvv.Electron_Edep>35.0 and
             fvv.BDTscore_1e1p>rse_scores[rse] ):
            rse_scores[rse] = fvv.BDTscore_1e1p
            rse_maxvtxid[rse] = fvv.vtxid
    elif selection in ["1m1p","1mu1p"]:
        pass

        
print "number in rse_scores dict: ",len(rse_scores)
            

rsev_dict = {}
print "Loop to define weight"
rse_filled = {}
nbad = 0
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
    if rse not in rse_filled and fvv.vtxid==rse_maxvtxid[rse]:
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
        evweight[0] = 0.0
        keepvtx[0] = 0

    if not goodrunlist[fvv.run]:
        nbad += 1
        evweight[0] = 0.0
        keepvtx[0] = 0
    
    tweight.Fill()

print "number of vertices in bad runs: ",nbad
tweight.Write()
fout.Close()

print "made: ",foutname
            
        
        
