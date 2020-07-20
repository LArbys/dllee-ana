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
evweight_1e1p = array.array('f',[0.0])
evscore_1e1p  = array.array('f',[0.0])
evweight_1m1p = array.array('f',[0.0])
evscore_1m1p  = array.array('f',[0.0])
keepvtx_1e1p  = array.array('i',[0])
keepvtx_1m1p  = array.array('i',[0])
tweight.Branch("run",run,"run/I")
tweight.Branch("subrun",subrun,"subrun/I")
tweight.Branch("event",event,"event/I")
tweight.Branch("vtxid",vtxid,"vtxid/I")
tweight.Branch("evweight_1e1p",evweight_1e1p,"evweight_1e1p/F")
tweight.Branch("evscore_1e1p", evscore_1e1p, "evscore_1e1p/F")
tweight.Branch("evweight_1m1p",evweight_1m1p,"evweight_1m1p/F")
tweight.Branch("evscore_1m1p", evscore_1m1p, "evscore_1m1p/F")
tweight.Branch("keepvtx_1e1p", keepvtx_1e1p, "keepvtx_1e1p/I")
tweight.Branch("keepvtx_1m1p", keepvtx_1m1p, "keepvtx_1m1p/I")

# need to tally max vertex for 1e1p
rse_scores_1e1p = {}
rse_maxvtxid_1e1p = {}

# need to tally max vertex for 1m1p
rse_scores_1m1p = {}
rse_minvtxid_1m1p = {}

print "Loop to define max RSE score"
for ientry in xrange(nentries):
    fvv.GetEntry(ientry)
    if ientry%10000==0:
        print " entry ",ientry
    rse = (fvv.run,fvv.subrun,fvv.event)
    if rse not in rse_scores_1e1p:
        # put in some default score
        rse_scores_1e1p[rse] = -1
        rse_maxvtxid_1e1p[rse] = -1
    if rse not in rse_scores_1m1p:
        rse_scores_1m1p[rse] = None
        rse_minvtxid_1m1p[rse] = -1

    # valid scores are only if other cuts pass
    if ( fvv.PassSimpleCuts==1 and
         #fvv.PassPMTPrecut==1 and
         fvv.MaxShrFrac>0.2 and
         fvv.Proton_Edep>60.0 and
         fvv.Electron_Edep>35.0 and
         fvv.BDTscore_1e1p>rse_scores_1e1p[rse] ):
        rse_scores_1e1p[rse]   = fvv.BDTscore_1e1p
        rse_maxvtxid_1e1p[rse] = fvv.vtxid

    if ( fvv.PassSimpleCuts==1 and
         #fvv.PassPMTPrecut==1 and
         fvv.MaxShrFrac<0.2 and
         fvv.OpenAng>0.5 and
         fvv.ChargeNearTrunk>0 and
         fvv.FailedBoost_1m1p!=1 and
         fvv.BDTscore_1mu1p_cosmic<0.7 and
         (fvv.BDTscore_1mu1p_nu>rse_scores_1m1p[rse] or rse_scores_1m1p[rse] is None)):
        rse_scores_1m1p[rse]   = fvv.BDTscore_1mu1p_nu
        rse_minvtxid_1m1p[rse] = fvv.vtxid
        

        
print "number in rse_scores_1m1p dict: ",len(rse_scores_1m1p)
print "number in rse_scores_1e1p dict: ",len(rse_scores_1e1p)
            

rsev_dict = {}
print "Loop to define weight"
rsev_filled = {}
nbad = 0
nrepeated = 0
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
    evscore_1e1p[0] = fvv.BDTscore_1e1p        
    evscore_1m1p[0] = fvv.BDTscore_1mu1p_nu
        
    if rsev not in rsev_filled:
        rsev_filled[rsev] = True        
        # 1e1p
        if fvv.vtxid==rse_maxvtxid_1e1p[rse]:
            evweight_1e1p[0] = 1.0
            keepvtx_1e1p[0]  = 1
        else:
            keepvtx_1e1p[0] = 0
            evweight_1e1p[0] = 0.0

        # 1m1p
        if fvv.vtxid==rse_minvtxid_1m1p[rse]:
            evweight_1m1p[0] = 1.0
            keepvtx_1m1p[0] = 1
        else:
            evweight_1m1p[0] = 0.0
            keepvtx_1m1p[0] = 0
    else:
        print "repeated RSEV! ",rsev
        nrepeated += 1
        evweight_1e1p[0] = 0.0
        keepvtx_1e1p[0] = 0
        evweight_1m1p[0] = 0.0
        keepvtx_1m1p[0] = 0

    if not goodrunlist[fvv.run]:
        nbad += 1
        evweight_1e1p[0] = 0.0
        keepvtx_1e1p[0] = 0
        evweight_1m1p[0] = 0.0
        keepvtx_1m1p[0] = 0
    
    tweight.Fill()

print "number of vertices in bad runs: ",nbad
print "number of repeated RSEV: ",nrepeated
tweight.Write()
fout.Close()

print "made: ",foutname
            
        
        
