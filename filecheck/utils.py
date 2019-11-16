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

def set_hist_style( hist, sample ):
    hist.SetLineColor( colors[sample] )
    hist.SetFillColor( colors[sample] )
    hist.SetFillStyle( fills[sample] )
    if sample in ["mcc9jan_bnb5e19"]:
        hist.SetLineWidth(2)

def scale_hist( hist, sample ):
    hist.Scale( scales[sample] )

def make_stack( hist_name, hist_dict ):
    hstack = rt.THStack("hstack","")    
    for sample in ["mcc9jan_extbnb","mcc9_v13_bnb_overlay_run1","mcc9_v13_overlay_dirt_run1"]:
        hstack.Add( hist_dict[sample] )
    return hstack
    
