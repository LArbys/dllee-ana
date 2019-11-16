import os,sys
import ROOT as rt

import utils

# Canvas
c = rt.TCanvas("cnvertices","Nvertices PE",1000,500)
c.Draw()

hname = "hnverticespe"
hists = {}
nbins = 10
minbin = 0
maxbin = 10

out = rt.TFile("temp.root","recreate")
# define hits
for sample in utils.samples:
    hn = hname+"_"+sample
    print hn    
    h = rt.TH1D( hn, ";num vertices per event", nbins, minbin, maxbin )
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
    trees[sample].Draw("nvertices>>%s"%(hn))
    prescale = hists[sample].Integral()
    utils.scale_hist( hists[sample], sample )
    print "  hist integral, ",sample,": prescale=",prescale," post-scale=",hists[sample].Integral()
    print "  pe above 0: ",trees[sample].GetEntries()*utils.scales[sample]    
    

# stacked prediction
hstack = utils.make_stack( "hnvertices_stack", hists )
hstack.SetTitle(";num vertex candidates in event")

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
#c.SetLogy(1)
#c.SetLogx(1)
c.Update()

raw_input()
                
