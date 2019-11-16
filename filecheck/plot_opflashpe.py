import os,sys
import ROOT as rt

import utils

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
for sample in utils.samples:
    hn = hname+"_"+sample
    print hn    
    h = rt.TH1D( hn, "", nbins, minbin, maxbin )
    utils.set_hist_style( h, sample )
    hists[sample] = h
    
out.ls()


# load trees, fill histogram
tree = "dlsummary"
rfile = {}
trees = {}
for sample in utils.samples:
    fname = "mcc9_v13/summarytree_dlmerged_"+sample+".root"
    rfile[sample] = rt.TFile( fname )
    trees[sample] = rfile[sample].Get(tree)
    print "Tree[%s]"%(sample),": entries=",trees[sample].GetEntries()
    out.cd()
    
    hn = hname+"_"+sample
    trees[sample].Draw("opflashpe>>%s"%(hn))
    prescale = hists[sample].Integral()
    utils.scale_hist( hists[sample], sample )
    print "  hist integral, ",sample,": prescale=",prescale," post-scale=",hists[sample].Integral()
    

# stacked prediction
hstack = utils.make_stack( "hopflashpe_stack", hists )

hmax_stack = hstack.GetMaximum()
hmax_bnb   = hists["mcc9jan_bnb5e19"].GetMaximum()

hmax = None
if hmax_stack>hmax_bnb:
    hmax = hstack
else:
    hmax = hists["mcc9jan_bnb5e19"]

# Draw hists
hmax.Draw("hist")
hstack.Draw("histE0same")
hists["mcc9jan_bnb5e19"].SetLineWidth(2)
hists["mcc9jan_bnb5e19"].Draw("E1same")

c.Draw()
c.SetLogy(1)
#c.SetLogx(1)
c.Update()

raw_input()
                
