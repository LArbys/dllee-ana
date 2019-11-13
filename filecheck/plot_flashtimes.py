import os,sys
import ROOT as rt

rt.gStyle.SetOptStat(0)

samples = ["mcc9jan_extbnb","mcc9jan_bnb5e19","mcc9_v13_bnb_overlay_run1"]

histname = "htflash"

rfile = {}
hists = {}

for sample in samples:
    fname = "mcc9_v13/summarytree_dlmerged_"+sample+".root"
    rfile[sample] = rt.TFile( fname )
    print fname
    h = rfile[sample].Get( histname )
    hists[sample] = h.Clone( histname+"_"+sample )
    if sample in ["mcc9jan_extbnb","mcc9_v13_bnb_overlay_run1"]:
        hists[sample].Reset()
        for i in range(1+24,hists[sample].GetXaxis().GetNbins()+1):
            hists[sample].SetBinContent( i-24, h.GetBinContent(i) )
    hists[sample].RebinX(4)
    hists[sample].SetTitle(";SimpleFlash time (usec);")
    print "hist integral, ",sample,": ",hists[sample].Integral()

extbnb_scale = (9571011+2220.0)/(12824524.0+15585.0)
hists["mcc9jan_extbnb"].Scale( extbnb_scale )

bnb_overlay_scale = 4.3e19/(2.0e18*24324/50.0)
hists["mcc9_v13_bnb_overlay_run1"].Scale( bnb_overlay_scale )

c = rt.TCanvas("ctflash","Flash Times",1000,500)

hists["mcc9jan_bnb5e19"].SetLineColor(rt.kBlack)
hists["mcc9jan_bnb5e19"].Draw("histE1")
hists["mcc9jan_extbnb"].SetLineColor(rt.kBlue)
hists["mcc9_v13_bnb_overlay_run1"].SetLineColor(rt.kRed)

#hists["mcc9jan_extbnb"].Draw("histE0same")
#hists["mcc9_v13_bnb_overlay_run1"].Draw("histE0same")

# stacked prediction
hstack = rt.THStack("hstack","")
hists["mcc9jan_extbnb"].SetFillColor(rt.kBlue)
hists["mcc9_v13_bnb_overlay_run1"].SetFillColor(rt.kRed)

hists["mcc9jan_extbnb"].SetFillStyle(3003)
hists["mcc9_v13_bnb_overlay_run1"].SetFillStyle(3003)

hstack.Add( hists["mcc9jan_extbnb"] )
hstack.Add( hists["mcc9_v13_bnb_overlay_run1"] )
hstack.Draw("histE0samE")
hists["mcc9jan_bnb5e19"].Draw("histE1same")

c.Draw()
c.Update()

raw_input()
                
