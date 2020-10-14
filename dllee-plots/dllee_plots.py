import os,sys
import ROOT as rt

"""
common modes
"""

###########
# RUN 1
###########
ntuple_dir="/home/twongjirad/working/larbys/datafiles/ntuples_v28-40_forNeutrino2020"

run1_files = { "mcbnbnuoverlay":[ntuple_dir+"/mcc9_v28_wctagger_bnboverlay_finalbdt.root"],
               "mcbnbintrinsic":[ntuple_dir+"/mcc9_v28_wctagger_nueintrinsics_finalbdt.root"],
               "extbnb":[ntuple_dir+"/mcc9_v28_wctagger_extbnb_finalbdt.root"],
               #"extbnb":[ntuple_dir+"/mcc9_v28_wctagger_extbnb_newbdt.root",
               #          ntuple_dir+"/mcc9_v29e_dl_run3_G1_extbnb.root"],
               "bnb":[ntuple_dir+"/mcc9_v28_wctagger_5e19_finalbdt.root"] }
run1_normfactors = {"mcbnbnuoverlay":4.71578587829e+20,
                    "mcbnbintrinsic":9.80336875336e+22,
                    "extbnb":22474918.0,
                    #"extbnb":22474918.0+39566274.0,
                    "bnb":1.0}

###########
# RUN 2
###########
ntuple_dir="/home/twongjirad/working/larbys/datafiles/ntuples_v28-40_forNeutrino2020"

run2_files = { "mcbnbnuoverlay":[ntuple_dir+"/mcc9_v29e_dl_run2_bnb_nu_overlay_finalbdt.root"],
               "mcbnbintrinsic":[ntuple_dir+"/mcc9_v29e_dl_run2_bnb_intrinsics_nue_overlay_finalbdt.root"],
               "extbnb":[ntuple_dir+"/mcc9_v29e_dl_run3_G1_extbnb_finalbdt.root"],
               "bnb":[ntuple_dir+"/mcc9_v29e_dl_run2_bnb_dlfilter_1m1p_v1_1_2b_fvv.root"] }
run2_normfactors = {"mcbnbnuoverlay":4.08963968669e+20,
                    "mcbnbintrinsic":9.2085012316e+22,
                    "extbnb":39566274.0,
                    "bnb":1.0}

###########
# RUN 3
###########
run3_files = { "mcbnbnuoverlay":[ntuple_dir+"/mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge_finalbdt.root"],
               "mcbnbintrinsic":[ntuple_dir+"/mcc9_v29e_dl_run3b_bnb_intrinsic_nue_overlay_nocrtremerge_finalbdt.root"],          
               "extbnb":[ntuple_dir+"/mcc9_v29e_dl_run3_G1_extbnb_finalbdt.root"],
               "bnb":[ntuple_dir+"/mcc9_v28_wctagger_run3_bnb1e19.root"]}
run3_normfactors = {"mcbnbnuoverlay":8.98773223801e20,
                    "mcbnbintrinsic":4.707047e22,
                    "extbnb":39566274.0,
                    "bnb":1.0}

DLLEE_DATA = {"run1":run1_files,
              "run2":run2_files,
              "run3":run3_files}
NORM_FACTORS={"run1":run1_normfactors,
              "run2":run2_normfactors,
              "run3":run3_normfactors}

#######################
# MC MODE DEFINITIONS
#######################
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
            
mcmode_colors = {"extbnb":rt.kGray,
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


def get_data(run):
    return DLLEE_DATA[run]


def get_scale_factors( run, bnbpot, bnbspills ):

    scales = {"mcbnbnuoverlay":bnbpot/NORM_FACTORS[run]["mcbnbnuoverlay"],
              "mcbnbintrinsic":bnbpot/NORM_FACTORS[run]["mcbnbintrinsic"],
              "extbnb":bnbspills/NORM_FACTORS[run]["extbnb"],
              "bnb":1.0}
    
    return scales

def get_dllee_trees( run, bnbfile ):

    files = get_data(run)
    if type(bnbfile) is list:
        files["bnb"] = bnbfile
    elif type(bnbfile) is str:
        files["bnb"] = [bnbfile]
    
    print "Load FVV trees"
    print files
    filenames = files.keys()

    trees = {}
    for name,path in files.items():
        trees[name] = rt.TChain("dlana/FinalVertexVariables")
        for f in files[name]:
            trees[name].Add( f )

    # add friend trees
    # MC weights
    print "Add MC Weight files"
    mcweighttrees = {}
    for samplename,fname in files.items():
        if "mc" in samplename:
            print samplename,fname
            for f in files[samplename]:
                mcweighttrees[samplename] = rt.TChain("mcweight")
                mcweighttrees[samplename].Add( "../auxdataprep/"+os.path.basename(f).replace(".root","_mcweight.root") )
            trees[samplename].AddFriend( mcweighttrees[samplename] )

    print "Load multivertex tree"
    multivtxtrees = {}
    for samplename,fname in files.items():
        print samplename,fname
        multivtxtrees[ samplename ] = rt.TChain("multivtxtree")
        for f in files[samplename]:
            multivtxtrees[ samplename ].Add( f.replace(".root","_multivtx.root") )
        trees[samplename].AddFriend( multivtxtrees[ samplename ] )
    
    return {"fvv":trees,"mcweight":mcweighttrees,"multivtx":multivtxtrees,"files":files}


def make_plots( plotdef_v, dllee_trees, scale, pause=True ):
    all_hists = {}
    canvas = {}

    trees = dllee_trees["fvv"]
    files = dllee_trees["files"]

    # split MC and data samples
    mcsamples = []
    datasamples = []
    for samplename,filename in files.items():
        if "mc" in samplename:
            mcsamples.append(samplename)
        else:
            datasamples.append(samplename)
    
    for plotdef in plotdef_v:

        if plotdef[3] is False:
            print "Skipping ",plotdef[0]
            continue
    
        print "PLOT: ",plotdef[0]
    
        canvas[plotdef[0]] = rt.TCanvas("c{}".format(plotdef[0]),plotdef[0],1200,600)
        tlen = rt.TLegend(0.0,0.5,0.6,1.0)        

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
            prescale = h.Integral()
            h.Scale( scale[datasample] )
            print (datasample),": prescale=",prescale," postscale=",h.Integral()
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

        datahists["extbnb"].SetFillColor( mcmode_colors["extbnb"] )
        ncoth.SetFillColor( mcmode_colors["ncoth"] )
        ncpi0.SetFillColor( mcmode_colors["ncpi0"] )
    
        hpred_stack.Add( datahists["extbnb"] )
        hpred_stack.Add( ncoth )
        hpred_stack.Add( ncpi0 )

        prediction += datahists["extbnb"].Integral()
        prediction += ncoth.Integral()
        prediction += ncpi0.Integral()
        
        for flavor in ["numu","nue"]:
            for ccmode in ["other","pi0","mec","qe"]:
                print "add : ",hcc_dict[(flavor,ccmode)].GetName()
                hhh = hcc_dict[(flavor,ccmode)]
                prediction += hhh.Integral()            
                hhh.SetFillColor( mcmode_colors["{}_cc_{}".format(flavor,ccmode)] )
                hpred_stack.Add( hhh )
                tlen.AddEntry( hhh,"%s %s (%.1f)"%(flavor,ccmode,hhh.Integral()),"F" )
        tlen.AddEntry( ncpi0,"NC #pi^{0} (%.1f)"%(ncpi0.Integral()), "F" )
        tlen.AddEntry( ncoth,"NC other (%.1f)"%(ncoth.Integral()), "F" )
        tlen.AddEntry( datahists["extbnb"],"EXTBNB (%.1f)"%(datahists["extbnb"].Integral()), "F" )
        
        canvas[plotdef[0]].Draw()
        hpred_stack.Draw("hist")
        tlen.AddEntry( hpred_stack,"Predicted: %.1f"%(prediction),"L")

        datahists["bnb"].SetLineColor( rt.kBlack )
        datahists["bnb"].SetLineWidth( 2 )
        tlen.AddEntry( datahists["bnb"],"BNB data (%d)"%(datahists["bnb"].Integral()), "L" )
        
        datahists["bnb"].Draw("E1same")
        
        tlen.Draw()
        
        canvas[plotdef[0]].Update()

        
        
        all_hists[plotdef[0]] = ( datahists, mchists, tlen )

        print "Prediction: ",prediction
        print "Data: ",datahists["bnb"].Integral()
        print "[Drew ",plotdef[0],"]"

        print "[enter] to continue"
        raw_input()

    return all_hists,canvas
    
    
