import os,sys
import ROOT as rt

rt.gStyle.SetOptStat(0)

import dllee_plots

## RUN 1:
#RUN = "run1"
# open 5e19 sample
#BNBPOT=4.403e+19
#BNBSPILLS=9776965.0
#BNBSPILLS=0.0
#BNBFILE=dllee_plots.ntuple_dir+"/mcc9_v28_wctagger_5e19.root"
#BNBFILE="merged_dlana_mcc9_v28_wctagger_5e19_numu-sideband_newbdt.root"
#BNBFILE=dllee_plots.ntuple_dir+"/mcc9_v28_wctagger_5e19_newbdt.root"
#BNBPOT=1.558e+20
#BNBSPILLS=37272955.0
#BNBFILE = "run1_C1_1e1p_lowBDT_sideband.v1_1_1.fvvonly.root"

## RUN 2: Low BDT
RUN = "run2"
BNBPOT=2.050e+20+6.507e+19
BNBSPILLS=49422124+19914275
BNBFILE = "mcc9_v29e_dl_run2_bnb_dlfilter_1m1p_v1_1_2b_fvv.root"

## RUN 3: 1m1p
#RUN = "run3"
#BNBFILE = "mcc9_v29e_dl_run3_G1_bnb_dlfilter_1m1p_v1_1_2b_fvv.root"
#BNBPOT=1.701e+20
#BNBSPILLS=43980680.0
## RUN 3: 1e19 open sample
#BNBFILE = dllee_plots.ntuple_dir+"/mcc9_v28_wctagger_run3_bnb1e19.root"
#BNBPOT=8.806e+18
#BNBSPILLS=2263559.0

dllee_trees  = dllee_plots.get_dllee_trees( RUN, BNBFILE )
scalefactors = dllee_plots.get_scale_factors( RUN, BNBPOT, BNBSPILLS )


numu_prebdt_cut = "PassSimpleCuts==1 "
numu_prebdt_cut += " && PassPMTPrecut==1 "
numu_prebdt_cut += " && MaxShrFrac<0.2 "
numu_prebdt_cut += " && ChargeNearTrunk>0.0 "
numu_prebdt_cut += " && FailedBoost_1m1p!=1 "
numu_prebdt_cut += " && keepvtx_1m1p>0 "
numu_bdt_cut = numu_prebdt_cut
numu_bdt_cut += " && BDTscore_1mu1p_nu<0.4 "
#numu_bdt_cut += " && BDTscore_1mu1p_nu<0.5"


print "PreBDT Cut: ",numu_prebdt_cut
print "BDT cut: ",numu_bdt_cut

plotdef_v = [ ("BDTscore_cosmic","TMath::Min(TMath::Max(BDTscore_1mu1p_cosmic,0.0),0.999)",numu_prebdt_cut,False,50,0,1.0),
              ("BDTscore_nu","TMath::Min(TMath::Max(BDTscore_1mu1p_nu,0.0),0.999)",numu_prebdt_cut,True,50,0,1.0),
              ("lowTotPE","TotPE",numu_bdt_cut,False,25,0,1000),
              ("TotPE","TotPE",numu_bdt_cut,False,20,0,10000),              
              ("Enu_1m1p","Enu_1m1p",numu_bdt_cut,True,24,0,2400),
              ("MaxShrFrac","TMath::Min(TMath::Max(MaxShrFrac,0.0),0.999)",numu_bdt_cut,False,50,0,1.0),
              #("PrecutBeamFirstTick","PrecutBeamFirstTick",numu_prebdt_cut,50,200.0,250.0),              
]

all_hists, canvas = dllee_plots.make_plots( plotdef_v, dllee_trees, scalefactors, pause=True )

raw_input()
