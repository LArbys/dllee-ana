import os,sys
import ROOT as rt

rt.gStyle.SetOptStat(0)

samples = ["mcc9jan_extbnb","mcc9jan_bnb5e19","mcc9_v13_bnb_overlay_run1","mcc9_v13_overlay_dirt_run1"]
scales = { "mcc9jan_extbnb":(9571011+2220.0)/(12824524.0+15585.0),
           "mcc9_v13_bnb_overlay_run1":4.3e19/(2.0e18*24324/50.0),
           "mcc9_v13_overlay_dirt_run1":4.3e19/(3.12362163789e+20),
           "mcc9jan_bnb5e19":1.0 }
colors = { "mcc9jan_extbnb":rt.kBlue,
           "mcc9_v13_bnb_overlay_run1":rt.kRed,
           "mcc9_v13_overlay_dirt_run1":rt.kGreen+2,
           "mcc9jan_bnb5e19":rt.kBlack }
fills = { "mcc9jan_extbnb":3003,
           "mcc9_v13_bnb_overlay_run1":3003,
           "mcc9_v13_overlay_dirt_run1":3003,
           "mcc9jan_bnb5e19":0 }

# Canvas
c = rt.TCanvas("copflash","Opflash PE",1000,500)
c.Draw()

hname = "hopflashpe"
hists = {}
nbins = 3000
minbin = 0.0
maxbin = 30e3

out = rt.TFile("temp.root","recreate")
# define hits
for sample in samples:
    hn = hname+"_"+sample
    print hn    
    h = rt.TH1D( hn, "", nbins, minbin, maxbin )
    hists[sample] = h
    hists[sample].SetLineColor( colors[sample] )
    hists[sample].SetFillColor( colors[sample] )
    hists[sample].SetFillStyle( fills[sample] )

out.ls()


# load trees, fill histogram
tree = "dlsummary"
rfile = {}
trees = {}
for sample in samples:
    fname = "mcc9_v13/summarytree_dlmerged_"+sample+".root"
    rfile[sample] = rt.TFile( fname )
    trees[sample] = rfile[sample].Get(tree)
    print "Tree[%s]"%(sample),": entries=",trees[sample].GetEntries()
    out.cd()
    
    hn = hname+"_"+sample
    trees[sample].Draw("opflashpe>>%s"%(hn),"opflashpe>0.0")
    prescale = hists[sample].Integral()
    hists[sample].Scale( scales[sample] )
    print "  hist integral, ",sample,": prescale=",prescale," post-scale=",hists[sample].Integral()
    

# stacked prediction
hstack = rt.THStack("hstack","")
hstack.Add( hists["mcc9jan_extbnb"] )
hstack.Add( hists["mcc9_v13_bnb_overlay_run1"] )
hstack.Add( hists["mcc9_v13_overlay_dirt_run1"] )

# Draw hists
hstack.Draw("histE0samE")
hists["mcc9jan_bnb5e19"].SetLineWidth(2)
hists["mcc9jan_bnb5e19"].Draw("E1same")

c.Draw()
c.Update()

raw_input()
                
