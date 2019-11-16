import os,sys

import ROOT as rt

rootfile = "mcc9_v13/summarytree_dlmerged_mcc9_v13_overlay_dirt_run1.root"

tree_pot = rt.TChain("dlpot")
tree_pot.Add( rootfile )

tree_pot.Print()

nentries = tree_pot.GetEntries()

pot = 0.0
for ientry in range(nentries):
    tree_pot.GetEntry(ientry)
    pot += tree_pot.pot

print "POT: ",pot
