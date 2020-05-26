import os,sys
from root_pandas import read_root

# we dump the run,subrun list of the BNB data sample in order to get the beam quality flags

ntuple_folder="~/working/larbys/datafiles/ntuples_v28-40_forNeutrino2020"
bnbsample="mcc9_v28_wctagger_run3_bnb1e19.root"

df_sample = read_root( ntuple_folder+"/"+bnbsample, "dlana/FinalVertexVariables", columns=["run","subrun"] )
df_rs =  df_sample.groupby( ['run','subrun'] ).size().rename(columns={0:'count'}).reset_index()
print df_rs

df_rs.to_root( bnbsample.replace(".root","_uniqueRS.root"), "rslist" )
