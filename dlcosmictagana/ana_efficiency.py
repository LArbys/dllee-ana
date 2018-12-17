import os,sys,time
import ROOT as rt
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
print "df_mc columns: ",df_mc.columns
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
print "df_flashana columns: ",df_flashana.columns
print "df_matchana columns: ",df_matchana.columns
print "df_flashana and df_matchana loading time: ",time.time()-loadmatchdf,"sec"

'''
df_flashana columns:  Index([u'run', u'subrun', u'event', u'flash_isneutrino', u'flash_intime',
       u'flash_isbeam', u'flash_isvisible', u'flash_crosstpc', u'flash_mcid',
       u'flash_truthqidx', u'flash_bestclustidx', u'flash_bestfmatch',
       u'flash_truthfmatch', u'flash_tick'],
'''
'''
df_matchana columns:  Index([u'run', u'subrun', u'event', u'flash_isneutrino', u'flash_intime',
       u'flash_isbeam', u'flash_isvisible', u'flash_crosstpc', u'flash_mcid',
       u'flash_tick', u'truthmatched', u'cutfailed', u'hypope', u'datape',
       u'dtickwin', u'maxdist', u'maxdist_wext', u'maxdist_noext', u'peratio',
       u'peratio_wext', u'peratio_noext', u'enterlen', u'fmatch',
       u'fmatch1_truth', u'fmatchm_frac1', u'fmatchm_frac2', u'fmatchm_mean',
       u'fmatchm_nsamples'],
      dtype='object')
'''

ev_mc    = df_mc.groupby( ["subrun","event"] )
ev_flash = df_flashana.groupby( ["subrun","event"] )
ev_match = df_matchana.groupby( ["subrun","event"] )

# =======================================================
# define hists
# ------------
tfout = rt.TFile("outfile_ana_efficiency.root","recreate")

hnue = { "all":  rt.TH1F("hnuE_all",";E^{true}_{#nu} (MeV)", 60,0,3000.0),
         "1e1p": rt.TH1F("hnuE_1e1p",";E^{true}_{#nu} (MeV)",60,0,3000.0),
         "1e1p_fv": rt.TH1F("hnuE_1e1p_fv",";E^{true}_{#nu} (MeV)",60,0,3000.0),
         "1e1p_visfv": rt.TH1F("hnuE_1e1p_visfv",";E^{true}_{#nu} (MeV)",60,0,3000.0),
         "1e1p_hascluster": rt.TH1F("hnuE_1e1p_hascluster",";E^{true}_{#nu} (MeV)",60,0,3000.0),
         "1e1p_selectmatch":  rt.TH1F("hnuE_1e1p_selectmatch",";E^{true}_{#nu} (MeV)", 60,0,3000.0) }

hfmatch = { "1e1p_visfv": rt.TH1F("hfmatch_1e1p_visfv",";fmatch",50,0,1.0),
            "intime_wtmatch":rt.TH1F("hfmatch_intime_wtmatch",";fmatch",50,0,1.0) }
hpos = {"1e1p_x": rt.TH1F("h1e1p_x",";x (cm)",50,0,256),
        "1e1p_visfv_x": rt.TH1F("h1e1p_visfv_x",";x (cm)",50,0,256),
        "1e1p_selected_x": rt.TH1F("h1e1p_selected_x",";x (cm)",50,0,256)}

hperatio = {"1e1p_peratio_visfv": rt.TH1D("h1e1p_peratio_visfv",";peratio;",50,0,5.0),
            "1e1p_peratio_hascluster": rt.TH1D("h1e1p_peratio_hascluster",";peratio;",50,0,5.0),
            "1e1p_peratio_selected": rt.TH1D("h1e1p_peratio_selected",";peratio;",50,0,5.0) }

hmaxdist = {"1e1p_maxdist_visfv": rt.TH1D("h1e1p_maxdist_visfv",";maxdist;",50,0,1.0),
            "1e1p_maxdist_hascluster": rt.TH1D("h1e1p_maxdist_hascluster",";maxdist;",50,0,1.0),
            "1e1p_maxdist_selected": rt.TH1D("h1e1p_maxdist_selected",";maxdist;",50,0,1.0) }

hcutfailed = {"1e1p_cutfailed_visfv":      rt.TH1I("h1e1p_cutfailed_visfv",";cutfailed;",11,-1,9),
              "1e1p_cutfailed_hascluster": rt.TH1I("h1e1p_cutfailed_hascluster",";cutfailed;",11,-1,9),
              "1e1p_cutfailed_selected":   rt.TH1I("h1e1p_cutfailed_selected",";cutfailed;",11,-1,9) }

denom = { "1e1p":0, "all": 0 }

numer = { "1e1p":0,
          "1e1p_fv":0,
          "1e1p_visflash":0,
          "1e1p_hascluster":0,
          "1e1p_selectmatch":0,
          "all_fv":0,
          "all_visflash":0,
          "all_selectmatch":0 }


ntotal_mc = 0
ntotal_hasmatches = 0

for name,mc_group in ev_mc:
    subrun=name[0]
    event=name[1]

    ntotal_mc += mc_group['event'].count() # should be one

    if subrun not in df_flashana['subrun'].values:
        continue
    if event not in df_flashana['event'].values:
        continue
    
    fg = ev_flash.get_group(name)
    mg = ev_match.get_group(name)
    ntotal_hasmatches += 1
    
    
    # data for one subrun,event
    #print "---------------------------------------------------------"
    #print name
    #print "---------------------------------------------------------"

    # prepare cuts
            
    # an observable neutrino is availabe
    vis_nuflash_df = fg[ (fg.flash_isneutrino==1) & (fg.flash_crosstpc==1) & (fg.flash_isvisible==1) & (fg.flash_intime==1) & (fg.flash_mcid>100000)]
    vis_nuflash = vis_nuflash_df['event'].count()    
    #print "  ",vis_nuflash_df
    #print "  vis_nuflash=",vis_nuflash

    #  cluster exists
    cluster_matched_df = vis_nuflash_df[ vis_nuflash_df.flash_truthqidx>=0 ]
    cluster_matched = cluster_matched_df['event'].count()
    #print "cluster_matched: ",cluster_matched
    #print "  ",cluster_matched_df
    
    # the intime neutrino match is selected
    selected_nuflash = mg[ (mg.flash_isneutrino==1) & (mg.truthmatched==1) & ( (mg.cutfailed==0) | (mg.cutfailed>=5) ) ]['event'].count()
    #print " selected_nuflash=",selected_nuflash

    # FV
    infv = mc_group[ (mc_group.x>10.0) & (mc_group.x<246) & (mc_group.y>-107.0) & (mc_group.y<107.0) & (mc_group.z>10.0) & (mc_group.z<1026) ]['event'].count()
    #print "  infv: ",infv

    # 1e1p
    l1p1 = (mc_group.l1p1==1).sum()==1
    #print "  1e1p: ",l1p1
    
    # MC variables
    nuEmev = mc_group['nuEmev'].values[0]
    xpos   = mc_group['x'].values[0]

    # truthcluster variable
    numatch_df = mg[ (mg.flash_isneutrino==1) & (mg.flash_intime==1) & (mg.truthmatched==1) ]
    print numatch_df
    peratio = 0
    maxdist = 0
    enterlen = 0
    cutfailed = -1
    if numatch_df['event'].count()>0:
        peratio  = numatch_df['peratio'].values[0]
        maxdist  = numatch_df['maxdist'].values[0]
        enterlen = numatch_df['enterlen'].values[0]
        cutfailed = int( numatch_df['cutfailed'].values[0] )

    # fill fmatch
    for fmatch in mg[ mg.flash_isneutrino==1 ]['fmatch'].values:
        hfmatch['1e1p_visfv'].Fill( fmatch )
    for fmatch in mg[ (mg.flash_isneutrino==1) & (mg.truthmatched==1) ]['fmatch'].values:
        hfmatch['intime_wtmatch'].Fill( fmatch )

    # file cut vars: pe ratio, maxdis, enterlen
    if l1p1==1 and vis_nuflash==1 and infv==1:
        hperatio['1e1p_peratio_visfv'].Fill(peratio)
        hmaxdist['1e1p_maxdist_visfv'].Fill(maxdist)
        #henterlen['1e1p_enterlen_visfv'].Fill(enterlen)
        hcutfailed['1e1p_cutfailed_visfv'].Fill(cutfailed)        
    if l1p1==1 and vis_nuflash==1 and infv==1 and cluster_matched==1:
        hperatio['1e1p_peratio_hascluster'].Fill(peratio)
        hmaxdist['1e1p_maxdist_hascluster'].Fill(maxdist)
        #henterlen['1e1p_enterlen_hascluster'].Fill(enterlen)
        hcutfailed['1e1p_cutfailed_hascluster'].Fill(cutfailed)        
    if l1p1==1 and vis_nuflash==1 and infv==1 and selected_nuflash==1:
        hperatio['1e1p_peratio_selected'].Fill(peratio)
        hmaxdist['1e1p_maxdist_selected'].Fill(maxdist)
        #henterlen['1e1p_enterlen_selected'].Fill(enterlen)
        hcutfailed['1e1p_cutfailed_selected'].Fill(cutfailed)

    # fill nu energy
    hnue['all'].Fill( nuEmev )
    
    # Start filling and counting
    denom['all']  += 1
    
    if l1p1==1:
        denom['1e1p'] += 1
        hnue['1e1p'].Fill( nuEmev )
        hpos['1e1p_x'].Fill( xpos )        

        numer["1e1p"] += 1
        if infv>=1:
            numer["1e1p_fv"] += 1
            hnue['1e1p_fv'].Fill( nuEmev )
            
            if vis_nuflash>0:
                numer["1e1p_visflash"] += 1
                hnue['1e1p_visfv'].Fill( nuEmev )
                hpos['1e1p_visfv_x'].Fill( xpos )
                
                if cluster_matched>0:
                    numer['1e1p_hascluster'] += 1
                if  selected_nuflash>0:
                    numer["1e1p_selectmatch"] += 1
                    hnue['1e1p_selectmatch'].Fill( nuEmev )
                    hpos['1e1p_selected_x'].Fill( xpos )                    



# end of event loop
print "Num Total MC events: ",ntotal_mc
print "Num Total events w/ match data: ",ntotal_hasmatches


cEnu = rt.TCanvas("c","NuE",800,600)
hnue['all'].Draw()
hnue['1e1p'].SetLineColor(rt.kBlue+3)
hnue['1e1p_fv'].SetLineColor(rt.kRed)
hnue['1e1p_visfv'].SetLineColor(rt.kMagenta)
hnue['1e1p_selectmatch'].SetFillColor(rt.kRed)

hnue['1e1p'].Draw("same")
hnue['1e1p_fv'].Draw("same")
hnue['1e1p_visfv'].Draw("same")
hnue['1e1p_selectmatch'].Draw("same")
cEnu.Update()
cEnu.Draw()

cfmatch = rt.TCanvas("cf","F-Match",800,600)
hfmatch['1e1p_visfv'].Draw()
hfmatch['intime_wtmatch'].SetFillColor( rt.kRed )
hfmatch['intime_wtmatch'].Draw("same")
cfmatch.Draw()

cxpos = rt.TCanvas("cxpos","x",800,600)
hpos['1e1p_x'].Draw()
hpos['1e1p_visfv_x'].SetLineColor(rt.kRed)
hpos['1e1p_selected_x'].SetFillColor(rt.kRed)
hpos['1e1p_visfv_x'].Draw("same")
hpos['1e1p_selected_x'].Draw("same")

print denom
print numer

for hdict in [hpos,hnue,hfmatch,hmaxdist,hperatio,hcutfailed]:
    for k,hist in hdict.items():
        hist.Write()

tfout.Close()
raw_input()

