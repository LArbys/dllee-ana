import os,sys,time

from root_pandas import read_root
import uproot

dataset = "mcc9tag2_nueintrinsic_corsika"
debug=True

# load data: flashmatch-ana file paths
flashana_inputdir="data/%s"%(dataset)
flashana_input_files=os.listdir(flashana_inputdir)
flashana_input_files.sort()
flashana_input_paths = [ "%s/%s"%(flashana_inputdir,x.strip()) for x in flashana_input_files ]

# load data: mc truth files paths
mctruth_inputdir="../skim_mctruth/data/%s/"%(dataset)
mctruth_input_files = os.listdir(mctruth_inputdir)
mctruth_input_files.sort()
mctruth_input_paths = [ "%s/%s"%(mctruth_inputdir,x.strip()) for x in mctruth_input_files ]

# align trees
start_aligntrees = time.time()
filepairs = {"mc":[],"match":[]}
nnotfound = 0
for flashtree in flashana_input_files:
    mctruth_path = mctruth_inputdir+"/"+flashtree.replace("flashmatch-ana","mcskim")
    if os.path.exists(mctruth_path):
        filepairs["mc"].append(mctruth_path)
        filepairs["match"].append(flashana_inputdir+"/"+flashtree)
    else:
        #print "could not find mcpair: ",mctruth_path
        nnotfound += 1
print "align trees: ",time.time()-start_aligntrees,"sec"
print "number of aligned trees: ",len(filepairs)
print "number not found: ",nnotfound

loadmcdf = time.time()
if not debug:
    df_mc = read_root( filepairs["mc"] )
else:
    df_mc = read_root( filepairs["mc"][:3] )
print "number of rows in df_mc: ",len(df_mc)
print "df_mc loading time: ",time.time()-loadmcdf,"sec"

loadmatchdf = time.time()
if not debug:
    df_flashana = read_root( filepairs["match"], "anaflashtree" )
    df_matchana = read_root( filepairs["match"], "matchana" )
else:
    df_flashana = read_root( filepairs["match"][:3], "anaflashtree" )
    df_matchana = read_root( filepairs["match"][:3], "matchana" )
    #df_flashana = uproot.open(flashana_inputdir+"/*.root")["anaflashtree"].pandas.df    
print "number of rows in df_flashana: ",len(df_flashana)
print "number of rows in df_matchana: ",len(df_matchana)
print "df_flashana and df_matchana loading time: ",time.time()-loadmatchdf,"sec"

## denominator
## in FV, 

