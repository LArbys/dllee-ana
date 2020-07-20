import os,sys
import ROOT as rt

rt.gStyle.SetOptStat(0)

import dllee_plots

## ====================================
## DATA DEFINITION
## ---------------

## RUN 1:
#RUN = "run1"
# open 5e19 sample
#BNBPOT=4.403e+19
#BNBSPILLS=9776965.0
#BNBFILE=dllee_plots.ntuple_dir+"/mcc9_v28_wctagger_5e19_finalbdt.root"

# RUN 1C LOW BDT
#BNBPOT=1.7302180e+20 # w/ GOOD BEAM FLAG CUT
#BNBSPILLS=38602759.0
#BNBFILE = "mcc9_v29e_dl_run1_C1_bnb_dlfilter_lowBDT_v1_1_3_fvv.root"

## RUN 2: Low BDT
RUN = "run2"
BNBPOT=2.642e+20-2.964e+19
BNBSPILLS=67599788.0-7089070.0
BNBFILE = ["mcc9_v29e_dl_run2_D2_bnb_dlfilter_highE_v1_1_3_fvv_nomakeup.root",
           "mcc9_v29e_dl_run2_E1_bnb_dlfilter_highE_v1_1_3_fvv.root"]

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


nue_bdt_cut = "PassSimpleCuts==1 "
#nue_bdt_cut += " && PassPMTPrecut==1 "
nue_bdt_cut += " && PassShowerReco==1 "
nue_bdt_cut += " && MaxShrFrac>0.2 "
nue_bdt_cut += " && Proton_Edep>60.0 "
nue_bdt_cut += " && Electron_Edep>35.0 "
nue_bdt_cut += " && keepvtx_1e1p==1"
nue_bdt_cut += " && BDTscore_1e1p>0.7"
#nue_bdt_cut += " && BDTscore_1e1p>0.05 && BDTscore_1e1p<0.7"
#nue_bdt_cut += " && BDTscore_1e1p>0.7"
#nue_bdt_cut += " && shower2_E_Y<60.0"
#nue_bdt_cut += " && PionPID_pix_v[2]<0.7"
#nue_bdt_cut += " && _pi0mass < 50 && MuonPID_int_v[2] < 0.2"
#nue_lowBDT_cut = nue_bdt_cut + " && BDTscore_1e1p<0.7"
nue_highe_cut = nue_bdt_cut + " && Enu_1e1p>700.0"

print "BDT Cut: ",nue_bdt_cut

plotdef_v = [ ("BDTscore","TMath::Min(TMath::Max(BDTscore_1e1p,0.0),0.999)",nue_highe_cut,False,20,0,1.0),
              ("lowTotPE","TotPE",nue_highe_cut,False,25,0,1000),
              ("TotPE","TotPE",nue_highe_cut,False,20,0,10000),              
              ("Enu_1e1p","Enu_1e1p",nue_bdt_cut,True,24,0,2400),
              ("MaxShrFrac","TMath::Min(TMath::Max(MaxShrFrac,0.0),0.999)",nue_highe_cut,False,50,0,1.0),
              ("MuonPID","TMath::Min(MuonPID_int_v[2],0.999)",nue_highe_cut,True,10,0,1.0),
              ("ProtonPID","TMath::Min(ProtonPID_int_v[2],0.999)",nue_highe_cut,True,10,0,1.0),
              ("ElectronPID","TMath::Min(EminusPID_int_v[2],0.999)",nue_highe_cut,True,10,0,1.0), 
              #("PrecutBeamFirstTick","PrecutBeamFirstTick",nue_bdt_cut,50,200.0,250.0),              
]

all_hists, canvas = dllee_plots.make_plots( plotdef_v, dllee_trees, scalefactors, pause=True )

raw_input()

## old
if True:
    sys.exit(0)


# plotdef_v = [ ("Enu_1e1p","Enu_1e1p",nue_bdt_cut,False,24,0,2400),
#               ("lowTotPE","TotPE",nue_bdt_cut,True,20,0,100),
#               ("TotPE","TotPE",nue_bdt_cut,True,20,0,10000),
#               ("SecondShowerE","shower2_E_Y",nue_bdt_cut,False,20,0,2000),
#               ("pionmpid","PionPID_pix_v[2]",nue_bdt_cut,False,20,0,1.0),
#               ("electronmpid","EminusPID_pix_v[2]",nue_bdt_cut,False,20,0,1.0),
#               ("muonmpid","MuonPID_pix_v[2]",nue_bdt_cut,False,20,0,1.0),
#               ("gammampid","GammaPID_pix_v[2]",nue_bdt_cut,False,20,0,1.0),              
#               #("MaxShrFrac","TMath::Min(TMath::Max(MaxShrFrac,0.0),0.999)",
#               #"PassSimpleCuts==1 && PassPMTPrecut==1 && PassShowerReco==1 && Proton_Edep>60.0 && Electron_Edep>35.0",20,0,1.0),
#               #("PrecutBeamFirstTick","PrecutBeamFirstTick",nue_bdt_cut,50,200.0,250.0),              
#               ("BDTscore","TMath::Min(TMath::Max(BDTscore_1e1p,0.0),0.999)",nue_bdt_cut + " && Enu_1e1p>700.0",False,20,0,1.0),
# ]

all_hists = {}
canvas = {}

for plotdef in plotdef_v:

    if plotdef[3]==False:
        print "Skipping ",plotdef[0]
        continue
    
    print "PLOT: ",plotdef[0]
    
    canvas[plotdef[0]] = rt.TCanvas("c{}".format(plotdef[0]),plotdef[0],800,500)

    # have to make large set of MC plots
    mchists = {}
    for mcsample in mcsamples:
        print " make mode hists for MC sample: ",mcsample
        for mcmode,modecut in mcmode_split.items():
            histname = "h{}_{}_{}".format(plotdef[0],mcsample,mcmode)
            cut = plotdef[2] + " && (%s)"%(modecut)
            cut = "xsec_corr_weight*(%s)"%(cut)
            h = rt.TH1F( histname,cut,plotdef[-3],plotdef[-2],plotdef[-1])
            trees[mcsample].Draw("{}>>{}".format(plotdef[1],histname),cut)
            h.Scale( scale[mcsample] )
            print (mcsample,mcmode)," :",h.Integral()
            mchists[(mcsample,mcmode)] = h

    # data hists
    datahists = {}
    for datasample in datasamples:
        print " make hists for data samples"
        histname = "h{}_{}".format(plotdef[0],datasample)
        cut = plotdef[2]
        h = rt.TH1F(histname,cut,plotdef[-3],plotdef[-2],plotdef[-1])
        trees[datasample].Draw("{}>>{}".format(plotdef[1],histname),cut)
        h.Scale( scale[datasample] )
        print (datasample),": ",h.Integral()
        datahists[datasample] = h

    # make prediction histograms
    # make a NC histograms
    ncall = rt.TH1F( "h{}_ncall".format(plotdef[0]), "MC nc all",   plotdef[-3],plotdef[-2],plotdef[-1] )
    ncpi0 = rt.TH1F( "h{}_ncpi0".format(plotdef[0]), "MC nc pi0",   plotdef[-3],plotdef[-2],plotdef[-1] )
    ncoth = rt.TH1F( "h{}_ncoth".format(plotdef[0]), "MC nc other", plotdef[-3],plotdef[-2],plotdef[-1] )        
    for mcsample in mcsamples:
        for mcmode in ["numu_nc_all","nue_nc_all"]:
            ncall.Add( mchists[(mcsample,mcmode)] )
        for mcmode in ["numu_nc_pi0","nue_nc_pi0"]:
            ncpi0.Add( mchists[(mcsample,mcmode)] )
    ncoth.Add(ncall)
    ncoth.Add(ncpi0,-1.0)
    print ncall.GetName(),": ",ncall.Integral()
    print ncpi0.GetName(),": ",ncpi0.Integral()
    print ncoth.GetName(),": ",ncoth.Integral()

    # for CC: we have modes all,QE,MEC,pi0,other x numu,nue
    hcc_dict = {}
    for flavor in ["numu","nue"]:
        hcc_not_oth = rt.TH1F("h{}_{}_cc_nototh".format(plotdef[0],flavor)," CC {} {} Not-Other".format(plotdef[0],flavor),plotdef[-3],plotdef[-2],plotdef[-1])        
        for ccmode in ["qe","mec","pi0","all"]:
            hcc = rt.TH1F("h{}_{}_{}".format(plotdef[0],flavor,ccmode),"CC {} {} {}".format(plotdef[0],flavor,ccmode),plotdef[-3],plotdef[-2],plotdef[-1])
            for mcsample in mcsamples:
                if flavor=="nue" and mcsample!="mcbnbintrinsic":
                    continue
                hcc.Add( mchists[(mcsample,"{}_cc_{}".format(flavor,ccmode))] )
            if ccmode!="all":
                hcc_not_oth.Add( hcc )
            print hcc.GetName(),": ",hcc.Integral()
            hcc_dict[(flavor,ccmode)] = hcc
        # other mode is a subtraction
        print hcc_not_oth.GetName(),": ",hcc_not_oth.Integral()
        hccother = rt.TH1F("h{}_{}_cc_oth".format(plotdef[0],flavor)," CC {} {} Other".format(plotdef[0],flavor),plotdef[-3],plotdef[-2],plotdef[-1])
        hccother.Add( hcc_dict[(flavor,"all")] )
        hccother.Add( hcc_not_oth, -1.0 )
        print hccother.GetName(),": ",hccother.Integral()
        hcc_dict[(flavor,"other")] = hccother

    # for MC prediction stack
    prediction = 0.0    
    hpred_stack = rt.THStack( "h{}_stack".format(plotdef[0]), plotdef[0] )

    datahists["extbnb"].SetFillColor( colors["extbnb"] )
    ncoth.SetFillColor( colors["ncoth"] )
    ncpi0.SetFillColor( colors["ncpi0"] )
    
    hpred_stack.Add( datahists["extbnb"] )
    hpred_stack.Add( ncoth )
    hpred_stack.Add( ncpi0 )

    prediction += datahists["extbnb"].Integral()
    prediction += ncoth.Integral()
    prediction += ncpi0.Integral()
    for flavor in ["numu","nue"]:
        for ccmode in ["other","pi0","mec","qe"]:
            print "add : ",hcc_dict[(flavor,ccmode)].GetName()
            prediction += hcc_dict[(flavor,ccmode)].Integral()            
            hcc_dict[(flavor,ccmode)].SetFillColor( colors["{}_cc_{}".format(flavor,ccmode)] )
            hpred_stack.Add( hcc_dict[(flavor,ccmode)] )
            
    datahists["bnb"].SetLineColor( rt.kBlack )
    datahists["bnb"].SetLineWidth( 2 )    
        

    canvas[plotdef[0]].Draw()
    hpred_stack.Draw("hist")
    datahists["bnb"].Draw("E1same")
    canvas[plotdef[0]].Update()

    print "Prediction: ",prediction
    print "Data: ",datahists["bnb"].Integral()
    print "[Drew ",plotdef[0],"]"

    print "[enter] to continue"
    raw_input()

raw_input()
