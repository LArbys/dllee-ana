import os,sys,json,time
import ROOT as rt
from root_pandas import read_root
import numpy as np

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
#mcpairs = [ ("mcc9_v28_wctagger_bnboverlay_finalbdt.root","weights_forCV_v40_bnb_nu_run1.root"),
#            ("mcc9_v28_wctagger_nueintrinsics_finalbdt.root","weights_forCV_v40_intrinsic_nue_run1.root") ]
#mcpairs = [ ("mcc9_v29e_dl_run3b_bnb_intrinsic_nue_overlay_nocrtremerge_finalbdt.root","weights_forCV_v40_intrinsic_nue_run3.root"),
#            ("mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge_finalbdt.root","weights_forCV_v40_bnb_nu_run3.root") ]
mcpairs = [ ("mcc9_v29e_dl_run2_bnb_nu_overlay_finalbdt.root","weights_forCV_v40_bnb_nu_run2.root"),
            ("mcc9_v29e_dl_run2_bnb_intrinsics_nue_overlay_finalbdt.root","weights_forCV_v40_intrinsic_nue_run2.root") ]


RSEE=['run','subrun','event','energy_index']
RSE=['run','subrun','event']
RSEVE = ['run','subrun','event','vtxid','energy_index']

N=100
def energy_index_weighttree( row ):
    #print row
    return np.round(row['nu_energy_true']*N).astype(np.int)
def energy_index_fvv( row ):
    return np.round(row['Enu_true']*N).astype(np.int)
def fix_null( row, df_weight ):
    #print row
    enu = row['Enu_true']
    q = "run==%d and subrun==%d and event==%d"%(row['run'],row['subrun'],row['event'])
    #print q
    g = df_weight.query(q)
    #print "query result: ",g
    g['diff'] = g.apply( lambda x:np.fabs(enu-x['nu_energy_true']),axis=1 )
    gsort = g.sort_values(by=['diff'])
    #print "gsort: ",gsort
    #print "gsort[xsec_corr_weight][0]: ",gsort['xsec_corr_weight'].iloc[0]
    return gsort['xsec_corr_weight'].iloc[0]

    

for samplefile,weightfile in mcpairs:
    print "======================================================================================"
    print "** make weights for: ",samplefile," with weight file: ",aux_folder+"/"+weightfile," **"
    #open weight rootfile in pandas, so we can get DB-like queries
    t_start = time.time()
    df_weight = read_root( aux_folder+"/"+weightfile, "eventweight_tree", columns=["run","subrun","event","nu_energy_true","xsec_corr_weight"] )
    dt_load_weights = time.time()-t_start
    print "loaded df_weight: ",dt_load_weights," secs"
    print "len(df_weight)=",len(df_weight)

    print "make new column with integer enery*1000"
    df_weight['energy_index'] = df_weight.apply( lambda row:energy_index_weighttree(row),axis=1 )
    df_weight = df_weight.set_index( RSEE )
    #print df_weight
    print "unique indices in weight file: ",len(df_weight.index.unique())
    dup_group = df_weight[df_weight.index.duplicated(keep=False)].groupby(RSEE)
    #print df_weight.index[df_weight.index.duplicated()].unique()
    print "number of duplicated RSEE indices in weight file: len(dup_group)=",len(dup_group)
    #for x in dup_group:
    #    #print x
    #    # break    
    df_weight = df_weight.reset_index().drop_duplicates().reset_index(drop=True)
    print "length of df_weight after duplicates removed: ",len(df_weight)
    print df_weight

    #test_group = df_weight.groupby(RSE).filter( lambda x: len(x)>1 )
    #test_group = df_weight.groupby(RSE)
    #for x in test_group:
    #    print x
    #    break
    #dup_group = df_weight.groupby(RSE).filter( lambda x: len(x)>1 )


    # index by run,subrun,event
    #df_weight = df_weight.set_index( RSE )
    #print df_weight

    t_start = time.time()
    df_sample = read_root( ntuple_folder+"/"+samplefile, "dlana/FinalVertexVariables", columns=["run","subrun","event","Enu_true","vtxid"] )
    dt_load_sampledf = time.time()-t_start
    print "loaded df_sample: ",len(df_sample)," entries in ",dt_load_sampledf," secs"
    print "add energy_index column to sample dataframe"
    df_sample['energy_index'] = df_sample.apply( lambda row:energy_index_fvv(row),axis=1 )

    df_sample = df_sample.set_index( RSEVE )
    dup_group = df_sample[df_sample.index.duplicated(keep=False)].groupby(RSEVE)
    print "number of duplicated RSEE indices in sample file: ",len(dup_group)
    for x in dup_group:
        print x
        break
    print df_sample

    df_sample = df_sample.reset_index()
    df_joined = df_sample.join( df_weight.set_index(RSEE), how='left', on=RSEE  )
    #df_joined = df_sample.join( df_weight.set_index(RSE), how='left', on=RSE, validate="one_to_one"  )
    #df_joined = df_sample.merge( df_weight, how='left',
    #                             #left_index=True, right_index=True,
    #                             on=RSEE, validate="many_to_one"  )
    df_null = df_joined[df_joined['xsec_corr_weight'].isnull()]
    print "DF NULL: "
    print df_null
    df_fix = df_null.apply( lambda row:fix_null(row,df_weight), axis=1 )
    print "DF FIX: "
    print df_fix
    #print df_fix.index

    for i,idx in enumerate(df_fix.index):
        #print df_joined.iloc[idx]['xsec_corr_weight']
        #print df_fix.iloc[i]
        df_joined.iloc[idx,df_joined.columns.get_loc('xsec_corr_weight')] = df_fix.iloc[i]
        #print "post: ",df_joined.iloc[idx,df_joined.columns.get_loc('xsec_corr_weight')] 
    df_joined['xsec_corr_weight'] = df_joined['xsec_corr_weight'].clip(upper=100.0,lower=0.0)


    df_joined.to_root( samplefile.replace(".root","_mcweight.root"), key="mcweight" )

    
