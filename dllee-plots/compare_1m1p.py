import os,sys

import ROOT as rt
rt.gStyle.SetOptStat(0)

"""
            if ( passprecuts==1
                 and dlanatree.PassSimpleCuts==1
                 and dlanatree.MaxShrFrac<0.2
                 and dlanatree.OpenAng>0.5
                 and dlanatree.ChargeNearTrunk>0
                 and dlanatree.FailedBoost_1m1p!=1
                 and dlanatree.Lepton_EdgeDist>15.0
                 and dlanatree.Proton_EdgeDist>15.0
                 and dlanatree.BDTscore_1mu1p_cosmic>0.0
                 and dlanatree.BDTscore_1mu1p_nu>0.0 ):

"""

datadir="~/working/larbys/datafiles/ntuples_v28-40_forNeutrino2020"
#fnames = [datadir+"/mcc9_v28_wctagger_run3_bnb1e19.root",
#          datadir+"/mcc9_v29e_dl_run3_G1_bnb_dlana_open1e19_fvv.root"]

#fnames = ["mcc9_v29e_dl_run3_G1_bnb_dlfilter_1m1p_fvv.root",
#          datadir+"/mcc9_v28_wctagger_run3_bnb1e19.root"]
#fnames = [datadir+"/mcc9_v29e_dl_run3b_bnb_nu_overlay_nocrtremerge.root",
#          "mcc9_v29e_dl_run3_G1_bnb_dlfilter_1m1p_fvv.root"]
fnames = [datadir+"/mcc9_v28_wctagger_5e19_newbdt.root",
          "merged_dlana_mcc9_v28_wctagger_5e19_numu-sideband_newbdt.root"]


drawstyle=["hist",
           "histE1"]

precut="PassSimpleCuts==1"
# for full cuts
precut+=" && PassPMTPrecut==1 "
precut+=" && MaxShrFrac<0.2 "
precut+=" && OpenAng>0.5  "
precut+=" && ChargeNearTrunk>0 "
precut+=" && FailedBoost_1m1p!=1 "
precut+=" && keepvtx_1m1p>=1 "
cut=precut
cut+=" && BDTscore_1mu1p_cosmic<0.7 "
cut+=" && BDTscore_1mu1p_nu<0.7 "
varlist = [ ("TotPE","TotPE",cut,100,0,10000),
            ("MaxShrFrac","TMath::Max(MaxShrFrac,0)",cut,100,0,1.0),
            ("OpenAng","OpenAng",cut,50,0,3.14159*2), 
            ("QTrunk","ChargeNearTrunk",cut,101,-100,1e3),
            ("LepEdgeDist","Lepton_EdgeDist",cut,50,0,200),
            ("ProtonEdgeDist","Proton_EdgeDist",cut,50,0,200),
            ("BDTcosmic","TMath::Min(BDTscore_1mu1p_cosmic,0.999)",precut,100,0.0,1.0),
            ("BDTnu","TMath::Min(BDTscore_1mu1p_nu,0.999)",precut,100,0.0,1.0),
            ("Enu_1m1p","TMath::Max(0,Enu_1m1p)",cut+" && Enu_1m1p<1000.0",20,0,2000.0),
            ("Simple","PassSimpleCuts","keepvtx_1m1p==1",5,0,5),
            ("Precut","PassPMTPrecut","keepvtx_1m1p==1",5,0,5) ]


rfiles = [ rt.TFile(f) for f in fnames ]
multivtxfiles = [ rt.TFile(f.replace(".root","_multivtx.root")) for f in fnames ]
trees = [ rfile.Get("dlana/FinalVertexVariables") for rfile in rfiles ]
multivtxtrees = [ rfile.Get("multivtxtree") for rfile in multivtxfiles ]
for t,m in zip(trees,multivtxtrees):
    t.AddFriend(m)
    print t,": ",t.GetEntries()

out = rt.TFile("out_temp.root","recreate")

hists = {}
canvas = {}
integrals = {}

for var in varlist:

    hists[var[0]] = []
    integrals[var[0]] = []
    c = rt.TCanvas("c{}".format(var[0]),var[0],800,600)
    c.Draw()

    hmax = -1
    maxval = 0.
    for i,tree in enumerate(trees):
        hname = "h{}_{}".format(var[0],i)
        hist = rt.TH1F(hname,var[0],var[-3],var[-2],var[-1])
        tree.Draw("{}>>{}".format(var[1],hname),var[2])
        integrals[var[0]].append( hist.Integral() )
        print hname,": ",integrals[var[0]][i]
        print "     cut: ",var[2]
        if hist.Integral()>0:
            s = 1.0/hist.Integral()
        else:
            s = 1.0
        hist.Scale(s)
        if maxval<hist.GetMaximum():
            maxval = hist.GetMaximum()
            hmax = i
        if i==1:
            hist.SetLineColor(rt.kRed)
        hists[var[0]].append(hist)


    hists[var[0]][hmax].Draw("hist")
    for n,h in enumerate(hists[var[0]]):
        h.Draw(drawstyle[n]+"same")
    c.Update()
    canvas[var[0]] = c

raw_input()


raw_input()
