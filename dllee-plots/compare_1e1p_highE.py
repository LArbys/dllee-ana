import os,sys

import ROOT as rt
rt.gStyle.SetOptStat(0)

datadir="~/working/larbys/datafiles/ntuples_v28-40_forNeutrino2020"

fnames = [datadir+"/mcc9_v29e_run3b_bnb_intrinsic_nue_overlay_nocrtremerge.root",
          "mcc9_v29e_dl_run3_G1_bnb_dlfilter_1e1p_highE_fvv.v1_1_0.root"]
#fnames = [datadir+"/mcc9_v29e_dl_run3_G1_bnb_dlana_open1e19_fvv.root",
#          "mcc9_v29e_dl_run3_G1_bnb_dlfilter_1e1p_lowBDT_partial_fvv.root"]


drawstyle=["hist",
           "histE1"]

cut="PassSimpleCuts==1"
# for full cuts
cut = "PassSimpleCuts==1 "
cut += " && PassPMTPrecut==1 "
cut += " && PassShowerReco==1 "
cut += " && MaxShrFrac>0.2 "
cut += " && Proton_Edep>60.0 "
cut += " && Electron_Edep>35.0 "
cut += " && Enu_1e1p>700.0"
cut += " && BDTscore_1e1p>0.9"
cut += " && keepvtx==1"

varlist = [ ("TotPE","TotPE",cut,100,0,10000),
            ("MaxShrFrac","TMath::Max(MaxShrFrac,0)",cut,100,0,1.0),
            ("OpenAng","OpenAng",cut,50,0,3.14159*2), 
            ("QTrunk","ChargeNearTrunk",cut,100,-100,10e3),
            ("ProtonEdep","Proton_Edep",cut,20,0,1000),
            ("ElectronEdep","Electron_Edep",cut,15,0,1500),
            ("BDT1e1p","BDTscore_1e1p",cut,100,0.0,1.0),
            ("Enu_1e1p","Enu_1e1p",cut,20,0.0,2000.0),
            ("keep","keepvtx","",5,0,5),
            ("Simple","PassSimpleCuts","",5,0,5),
            ("Precut","PassPMTPrecut","",5,0,5) ]


rfiles = [ rt.TFile(f) for f in fnames ]
multivtxfiles = [ rt.TFile(f.replace(".root","_multivtx.root")) for f in fnames ]
trees = [ rfile.Get("dlana/FinalVertexVariables") for rfile in rfiles ]
multivtxtrees = [ rfile.Get("multivtxtree") for rfile in multivtxfiles ]
for t,m in zip(trees,multivtxtrees):
    t.AddFriend(m) 

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
        histcut = var[2]
        print hname," [",var[1],"]: ",histcut
        tree.Draw("{}>>{}".format(var[1],hname),histcut)
        integrals[var[0]].append( hist.Integral() )
        print hname,": ",integrals[var[0]][i]        
        s = 1.0/hist.Integral()
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
