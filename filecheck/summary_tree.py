import os,sys, array

import ROOT as rt
from larlite import larlite
from larcv import larcv

dataset = "dlmergedsparsessnet_mcc9jan_extbnb"
filelist = open("filelists/%s.list"%(dataset),'r')
jobid=0
ismc=False
nfiles = 10

lfilelist = filelist.readlines()
print "Number of files in filelist: ",len(lfilelist)


 # SETUP INPUT
start=jobid*nfiles
end  =(jobid+1)*nfiles

if end>len(lfilelist):
    end = len(lfilelist)

potchain = rt.TChain("potsummary_generator_tree")

ioll = larlite.storage_manager( larlite.storage_manager.kREAD )
iolcv = larcv.IOManager( larcv.IOManager.kREAD, "klarcv", larcv.IOManager.kTickForward )

for f in lfilelist[start:end]:
    if ".root" not in f:
        continue
    print "ana: ",f.strip()
    os.system("ln -s %s %s"%(f.strip(),os.path.basename(f.strip())))
    potchain.Add( os.path.basename(f.strip()) )
    ioll.add_in_filename( os.path.basename(f.strip()) )
    iolcv.add_in_file( os.path.basename(f.strip()) )
    
ioll.open()
iolcv.initialize()

out = rt.TFile("output_filecheck_plots_%s_%03d.root"%(dataset,jobid),"recreate")

ttree = rt.TTree("dlsummary","MC File statistics")
tpot  = rt.TTree("dlpot",    "MC File statistics")
thflashtime = rt.TH1D("htflash","",3000,-500*0.015625,2500*0.015625)

# summary vars
idx = array.array('i',[0])
run    = array.array('i',[0])
subrun = array.array('i',[0])
event  = array.array('i',[0])
opflashpe = array.array('f',[0])
numvertices = array.array('i',[0])

# pot vars
pot = array.array('f',[0.0])

ttree.Branch("idx",idx,"idx/I")
ttree.Branch("run",run,"run/I")
ttree.Branch("subrun",subrun,"subrun/I")
ttree.Branch("event",event,"event/I")
ttree.Branch("opflashpe",opflashpe,"opflashpe/F")

tpot.Branch("pot",pot,"pot/F")


# POT
pot[0] = 0.0
if ismc:
    for ientry in pot_table.GetEntries():
        pot_table.GetEntry(ientry)
        pot[0] = pot_table.potsummary_generator_branch.totpot

# opflash
nentries = ioll.get_entries()
nentries_lcv = iolcv.get_n_entries()

for ientry in xrange(nentries):
    print "[Entry ",ientry,"]"
    ioll.go_to(ientry)
    iolcv.read_entry(ientry)

    # opflash
    opflashpe[0] = 0.0
    flash_v = ioll.get_data( larlite.data.kOpFlash, "simpleFlashBeam" )
    for iflash in xrange(flash_v.size()):
        flash = flash_v.at(iflash)
        tusec = flash.Time()
        thflashtime.Fill( tusec )
        #print "[%d] tusec=%.2f pe=%.2f"%(iflash,tusec,flash.TotalPE())
        #if tusec>=190*0.015625 and tusec<=210*0.015625 and opflashpe[0]==0.0:
        if tusec>=4.0 and tusec<=6.0 and opflashpe[0]==0.0:
            opflashpe[0] = flash.TotalPE()


    run[0] = ioll.run_id()
    subrun[0] = ioll.subrun_id()
    event[0] = ioll.event_id()

    idx[0] = run[0]*10000 + event[0]

    ttree.Fill()
        
print "WRITE"
out.Write()
print "DONE"
