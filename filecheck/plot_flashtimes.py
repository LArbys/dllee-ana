import os,sys
import ROOT as rt

samples = ["mcc9jan_extbnb","mcc9jan_bnb5e19","mcc9_v13_bnb_overlay_run1"]

histname = "htflash"

rfile = {}
hists = {}

for sample in samples:
    fname = "mcc9_v13/summarytree_dlmerged_"+sample+".root"
    rfile[sample] = rt.TFile( fname )
    print fname
    hists[sample] = rfile[sample].Get( histname ).Clone( histname+"_"+sample )
    print "hist integral, ",sample,": ",hists[sample].Integral()

extbnb_scale = (9571011+2220.0)/(12824524.0+15585.0)
hists["mcc9jan_extbnb"].Scale( extbnb_scale )

c = rt.TCanvas("ctflash","Flash Times",1000,500)

hists["mcc9jan_bnb5e19"].SetLineColor(rt.kRed)
hists["mcc9jan_bnb5e19"].Draw("hist")
hists["mcc9jan_extbnb"].Draw("histsame")

c.Draw()
c.Update()

raw_input()
                
