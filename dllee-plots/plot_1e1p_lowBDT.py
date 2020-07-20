import os,sys
import ROOT as rt

rt.gStyle.SetOptStat(0)

import dllee_plots

## RUN 1:
RUN = "run1"
# open 5e19 sample
#BNBPOT=4.403e+19
#BNBSPILLS=9776965.0
#BNBFILE=dllee_plots.ntuple_dir+"/mcc9_v28_wctagger_5e19_finalbdt.root"

# RUN 1CL LOW BDT
BNBPOT=1.7302180e+20 # w/ GOOD BEAM FLAG CUT
BNBSPILLS=38602759.0
BNBFILE = "mcc9_v29e_dl_run1_C1_bnb_dlfilter_lowBDT_v1_1_3_fvv.root"

## RUN 2: Low BDT
#RUN = "run2"
#BNBPOT=1.63e+20
#BNBSPILLS=39123798.0*1.15
#BNBFILE = "run2_D2_1e1p_lowBDT_sideband.v1_1_1.fvvonly.root"

## RUN 3: lowBDT
#RUN = "run3"
#BNBFILE = dllee_plots.ntuple_dir+"/mcc9_v29e_dl_run3_G1_dlfilter_1e1p_lowBDT_v1_1_1_refilter_fvv_v2.root"
#BNBPOT=1.701e+20
#BNBSPILLS=43980680.0
## RUN 3: 1e19 open sample
#BNBFILE = dllee_plots.ntuple_dir+"/mcc9_v28_wctagger_run3_bnb1e19.root"
#BNBPOT=8.806e+18
#BNBSPILLS=2263559.0

dllee_trees  = dllee_plots.get_dllee_trees( RUN, BNBFILE )
scalefactors = dllee_plots.get_scale_factors( RUN, BNBPOT, BNBSPILLS )


nue_prebdt_cut = "PassSimpleCuts==1 "
#nue_prebdt_cut += " && PassPMTPrecut==1 "
nue_prebdt_cut += " && PassShowerReco==1 "
nue_prebdt_cut += " && MaxShrFrac>0.2 "
nue_prebdt_cut += " && Proton_Edep>60.0 "
nue_prebdt_cut += " && Electron_Edep>35.0 "
nue_prebdt_cut += " && keepvtx_1e1p==1"
#nue_prebdt_cut += " && BDTscore_1e1p>0.05 && BDTscore_1e1p<0.7"
#nue_prebdt_cut += " && BDTscore_1e1p>0.7"
#nue_prebdt_cut += " && shower2_E_Y<60.0"
#nue_prebdt_cut += " && PionPID_pix_v[2]<0.7"
#nue_prebdt_cut += " && _pi0mass < 50 && MuonPID_int_v[2] < 0.2"
nue_lowBDT_cut = nue_prebdt_cut + " && BDTscore_1e1p<0.7"

print "PreBDT Cut: ",nue_prebdt_cut
print "BDT cut: ",nue_lowBDT_cut

plotdef_v = [ ("BDTscore","TMath::Min(TMath::Max(BDTscore_1e1p,0.0),0.999)",nue_prebdt_cut,True,20,0,1.0),
              ("lowTotPE","TotPE",nue_lowBDT_cut,False,25,0,1000),
              ("TotPE","TotPE",nue_lowBDT_cut,False,20,0,10000),              
              ("Enu_1e1p","Enu_1e1p",nue_lowBDT_cut,True,24,0,2400),
              ("MaxShrFrac","TMath::Min(TMath::Max(MaxShrFrac,0.0),0.999)",nue_lowBDT_cut,False,50,0,1.0),
              ("MuonPID","TMath::Min(MuonPID_int_v[2],0.999)",nue_lowBDT_cut,True,50,0,1.0),
              ("ProtonPID","TMath::Min(ProtonPID_int_v[2],0.999)",nue_lowBDT_cut,True,50,0,1.0),
              ("ElectronPID","TMath::Min(EminusPID_int_v[2],0.999)",nue_lowBDT_cut,True,50,0,1.0), 
              #("PrecutBeamFirstTick","PrecutBeamFirstTick",nue_prebdt_cut,50,200.0,250.0),              
]

all_hists, canvas = dllee_plots.make_plots( plotdef_v, dllee_trees, scalefactors, pause=True )

raw_input()
