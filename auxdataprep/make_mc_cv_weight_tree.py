import os,sys,json,time
import ROOT as rt
from root_pandas import read_root

ntuple_folder="~/working/larbys/datafiles/ntuples_v28-40_forNeutrino2020"
"""
dlfilter_numu_mcc9_v28_wctagger_bnb_nu_overlay_test.root   mcc9_v29e_dl_run3b_intrinsic_nue_LowE.root                                 mcc9_v29e_run1_bnb_nu_overlay_LowE.root
dlfilter_run3b_intrinsic_nue_LowE_1e1p_signal_test.root    mcc9_v29e_dl_run3b_intrinsic_nue_LowE_ssnetlow.root                        mcc9_v29e_run3b_bnb_intrinsic_nue_overlay_nocrtremerge.root
mcc9_v28_wctagger_bnb_nu_overlay_test.root                 mcc9_v29e_dl_run3b_intrinsic_nue_LowE_vtxthreshold.root                    mcc9_v29e_run3b_bnb_nu_overlay_LowE.root
mcc9_v28_wctagger_nueintrinsics.root                       mcc9_v29e_dl_run3b_intrinsic_nue_overlay_nocrtremerge_old_wshowerbug.root  mcc9_v40a_dl_run3b_bnb_intrinsic_nue_overlay_wiremodX.root
mcc9_v28_wctagger_run3_bnb1e19.root                        mcc9_v29e_dl_run3b_intrinsic_nue_overlay_nocrtremerge.root                 mcc9_v40a_dl_run3b_intrinsic_nue_CV.root
mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge.root        mcc9_v29e_dl_run3_G1_extbnb.root                                           merged_dlreco_1feb96c4-e96a-4d9a-82d6-6830d421b699.root
mcc9_v29e_dl_run3b_intrinsic_nue_LowE_old_wshowerbug.root  mcc9_v29e_run1_bnb_intrinsic_nue_LowE.root                                 out_larbysmc.root
"""


aux_folder="~/working/larbys/datafiles/aux_v28-40_forNeutrino2020"
"""
twongjirad@blade:~/working/larbys/dllee-ana/auxdataprep$ ls ~/working/larbys/datafiles/aux_v28-40_forNeutrino2020/
weights_forCV_v40_bnb_nu_run1.root  weights_forCV_v40_dirt_nu_run1.root  weights_forCV_v40_intrinsic_nue_run1.root
weights_forCV_v40_bnb_nu_run3.root  weights_forCV_v40_dirt_nu_run3.root  weights_forCV_v40_intrinsic_nue_run3.root
"""
"""
(TFile *) 0x555579ce5240
root [1] .ls
TFile**		/home/twongjirad/working/larbys/datafiles/aux_v28-40_forNeutrino2020/weights_forCV_v40_bnb_nu_run3.root	
 TFile*		/home/twongjirad/working/larbys/datafiles/aux_v28-40_forNeutrino2020/weights_forCV_v40_bnb_nu_run3.root	
  KEY: TTree	eventweight_tree;141	eventweight_tree
  KEY: TTree	eventweight_tree;140	eventweight_tree
"""

#mcpairs = [ ("mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge.root","weights_forCV_v40_bnb_nu_run3.root") ]
#mcpairs = [ ("mcc9_v29e_run3b_bnb_intrinsic_nue_overlay_nocrtremerge.root","weights_forCV_v40_intrinsic_nue_run3.root") ]
#mcpairs = [ ("mcc9_v28_wctagger_nueintrinsics.root","weights_forCV_v40_intrinsic_nue_run1.root"),
#            ("mcc9_v28_wctagger_bnboverlay.root","weights_forCV_v40_bnb_nu_run1.root")]
mcpairs = [ ("mcc9_v28_wctagger_bnboverlay_newbdt.root","weights_forCV_v40_bnb_nu_run1.root"),
            ("mcc9_v28_wctagger_nueintrinsics_newbdt.root","weights_forCV_v40_intrinsic_nue_run1.root") ]

RSE=['run','subrun','event']

for samplefile,weightfile in mcpairs:
    print "make weights for: ",samplefile
    #open weight rootfile in pandas, so we can get DB-like queries
    t_start = time.time()
    df_weight = read_root( aux_folder+"/"+weightfile, "eventweight_tree", columns=["run","subrun","event","xsec_corr_weight"] )
    dt_load_weights = time.time()-t_start
    print "loaded df_weight: ",dt_load_weights," secs"

    # index by run,subrun,event
    #df_weight = df_weight.set_index( RSE )
    #print df_weight

    t_start = time.time()
    df_sample = read_root( ntuple_folder+"/"+samplefile, "dlana/FinalVertexVariables", columns=["run","subrun","event","vtxid"] )
    dt_load_sampledf = time.time()-t_start
    print "loaded df_sample: ",len(df_sample)," entries in ",dt_load_sampledf," secs"

    df_joined = df_sample.join( df_weight.set_index(RSE), how='left', on=RSE  )
    df_joined['xsec_corr_weight'] = df_joined['xsec_corr_weight'].clip(upper=100.0,lower=0.0)

    df_joined.to_root( samplefile.replace(".root","_mcweight.root"), key="mcweight" )
    
