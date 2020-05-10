import os,sys
import ROOT as rt

rt.gStyle.SetOptStat(0)

ntuple_dir="~/working/larbys/datafiles/ntuples_v28-40_forNeutrino2020"
files = { "mcbnbnuoverlay":ntuple_dir+"/mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge.root",
          "mcbnbintrinsic":ntuple_dir+"/mcc9_v29e_run3b_bnb_intrinsic_nue_overlay_nocrtremerge.root",          
          "extbnb":ntuple_dir+"/mcc9_v29e_dl_run3_G1_extbnb.root",
          "bnb":ntuple_dir+"/mcc9_v28_wctagger_run3_bnb1e19.root" }
files["bnb"] = "mcc9_v29e_dl_run3_G1_dlfilter_1e1p_lowBDT_v1_1_1_refilter_fvv.root"
#BNBPOT=8.786e18
#BNBSPILLS=2263559.0
#BNBPOT=7.102e+18
#BNBSPILLS=1822131.0
#BNBPOT=7.102e+19
#BNBSPILLS=1822131.0
#BNBPOT=1.03e20
#BNBSPILLS=26612977.0
BNBPOT=1.701e+20
BNBSPILLS=43980680.0

# get MC samples (must have 'mc' in name)
mcsamples = []
datasamples = []
for samplename,filename in files.items():
    if "mc" in samplename:
        mcsamples.append(samplename)
    else:
        datasamples.append(samplename)

scale = {"mcbnbnuoverlay":BNBPOT/8.98773223801e20,
         "mcbnbintrinsic":BNBPOT/4.707047e22,
         "extbnb":BNBSPILLS/39566274.0,
         "bnb":1.0}

mcmode_split = {"numu_cc_qe":"(interactionType==1001 && currentType==0 && abs(MC_parentPDG)==14)",
                "numu_cc_mec":"(genieMode==10 && currentType==0 && abs(MC_parentPDG)==14)",
                "nue_cc_qe":"(interactionType==1001 && currentType==0 && abs(MC_parentPDG)==12)",
                "nue_cc_mec":"(genieMode==10 && currentType==0 && abs(MC_parentPDG)==12)",
                "numu_cc_pi0":"currentType==0 && interactionType!=1001 && genieMode!=10 && npi0>0 && (abs(MC_parentPDG)==14)",
                "nue_cc_pi0":"currentType==0 && interactionType!=1001 && genieMode!=10 && npi0>0 && (abs(MC_parentPDG)==12)",
                "numu_nc_pi0":"currentType==1 && interactionType!=1001 && genieMode!=10 && npi0>0 && (abs(MC_parentPDG)==14)",
                "nue_nc_pi0":"currentType==1 && interactionType!=1001 && genieMode!=10 && npi0>0 && (abs(MC_parentPDG)==12)",
                "numu_cc_all":"currentType==0 && (abs(MC_parentPDG)==14)",
                "nue_cc_all":"currentType==0 && (abs(MC_parentPDG)==12)",
                "numu_nc_all":"currentType==1 && (abs(MC_parentPDG)==14)",
                "nue_nc_all":"currentType==1 && (abs(MC_parentPDG)==12)"}
            
colors = {"extbnb":rt.kGray,
          "ncpi0":rt.kGreen-9,
          "ncoth":rt.kGreen+2,
          "numu_cc_qe":rt.kRed,
          "numu_cc_mec":rt.kRed+3,
          "numu_cc_pi0":rt.kOrange-3,
          "numu_cc_other":rt.kRed-10,
          "nue_cc_qe":rt.kBlue,
          "nue_cc_mec":rt.kBlue+3,
          "nue_cc_pi0":rt.kCyan+2,
          "nue_cc_other":rt.kBlue-10,
          "bnb":rt.kBlack}

print "SCALE FACTORS"
print scale
         
filenames = files.keys()

print "Load FVV trees"
trees = {}
for name,path in files.items():
    trees[name] = rt.TChain("dlana/FinalVertexVariables")
    trees[name].Add( files[name] )

# add friend trees
# MC weights
print "Add MC Weight files"
mcweighttrees = {}
for samplename,fname in files.items():
    if "mc" in samplename:
        mcweighttrees[samplename] = rt.TChain("mcweight")
        mcweighttrees[samplename].Add( "../auxdataprep/"+os.path.basename(fname).replace(".root","_mcweight.root") )
        trees[samplename].AddFriend( mcweighttrees[samplename] )

print "Load multivertex tree"
multivtxtrees = {}
for samplename,fname in files.items():
    multivtxtrees[ samplename ] = rt.TChain("multivtxtree")
    multivtxtrees[ samplename ].Add( fname.replace(".root","_multivtx.root") )
    trees[samplename].AddFriend( multivtxtrees[ samplename ] )



nue_prebdt_cut = "PassSimpleCuts==1 "
nue_prebdt_cut += " && PassPMTPrecut==1 "
nue_prebdt_cut += " && PassShowerReco==1 "
nue_prebdt_cut += " && MaxShrFrac>0.2 "
nue_prebdt_cut += " && Proton_Edep>60.0 "
nue_prebdt_cut += " && Electron_Edep>35.0 "
nue_prebdt_cut += " && keepvtx==1"
#nue_prebdt_cut += " && BDTscore_1e1p>0.7"

plotdef_v = [ ("Enu_1e1p","Enu_1e1p",nue_prebdt_cut+" && BDTscore_1e1p<0.7",24,0,2400),
              #("MaxShrFrac","TMath::Min(TMath::Max(MaxShrFrac,0.0),0.999)",
              #"PassSimpleCuts==1 && PassPMTPrecut==1 && PassShowerReco==1 && Proton_Edep>60.0 && Electron_Edep>35.0",20,0,1.0),
              #("PrecutBeamFirstTick","PrecutBeamFirstTick",nue_prebdt_cut,50,200.0,250.0),              
              ("BDTscore","TMath::Min(TMath::Max(BDTscore_1e1p,0.0),0.999)",nue_prebdt_cut,20,0,1.0),
]

all_hists = {}
canvas = {}

for plotdef in plotdef_v:

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
