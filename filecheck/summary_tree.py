import os,sys, array, argparse

parser = argparse.ArgumentParser( "Summary Tree Maker" )
parser.add_argument("--jobid","-j",required=True,type=int,help="JOB ARRAY ID")
parser.add_argument("--sample","-s",required=True,type=str,help="Sample Name")
parser.add_argument("--output","-o",default=None,type=str,help="Output file name")
parser.add_argument("--nfiles","-n",default=1,type=int,help="Number of files per job")
parser.add_argument("--ismc","-mc",default=False,action='store_true',help="File is MC")
parser.add_argument("--ext","-ext",default=False,action='store_true',help="EXT trigger sample")
parser.add_argument("--flist-dir","-fd",default="../../../filelists",type=str,help="location of filelists")

args = parser.parse_args()

import ROOT as rt
from larlite import larlite
from larcv import larcv

dataset = "dlmergedsparsessnet_mcc9jan_extbnb"
jobid=0
ismc=False
nfiles = 10

dataset = args.sample
jobid   = args.jobid
ismc    = args.ismc
nfiles  = args.nfiles

flist_path = args.flist_dir+"/%s.list"%(dataset)

filelist = open(flist_path,'r')
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

fbad = open("bad_dlmerged_list.txt",'w')

for f in lfilelist[start:end]:
    if ".root" not in f:
        continue

    print "process ",f.strip()
    basename = os.path.basename(f.strip())
    os.system("ln -s %s %s"%(f.strip(),basename))

    # check file first
    isgood = True
    try:
    #if True:
        fff = rt.TFile( basename, 'read' )
        wire_tree = fff.Get("image2d_wire_tree")
        tracker_tree = fff.Get("track_trackReco_tree")
        vertex_tree  = fff.Get("pgraph_test_tree")
        shower_tree  = fff.Get("shower_showerreco_tree")

        nimages = wire_tree.GetEntries()
        if tracker_tree.GetEntries()!=nimages or tracker_tree.GetEntries()!=nimages or shower_tree.GetEntries()!=nimages or vertex_tree.GetEntries()!=nimages:
            isgood = False
            print "number of entries do not match"

        fff.Close()
    
    except:
        print "could not parse file: ",basename
        isgood = False

    if not isgood:
        print "problem with file: ",basename
        print>>fbad,basename
        continue


    potchain.Add( basename )
    ioll.add_in_filename( basename )
    iolcv.add_in_file( basename )
    
ioll.open()
iolcv.initialize()

out = rt.TFile("output_filecheck_plots_%s_%04d.root"%(dataset,jobid),"recreate")

ttree = rt.TTree("dlsummary","MC File statistics")
tpot  = rt.TTree("dlpot",    "MC File statistics")
thflashtime = rt.TH1D("htflash","",3000,-500*0.015625,2500*0.015625)

# summary vars
idx = array.array('i',[0])
run    = array.array('i',[0])
subrun = array.array('i',[0])
event  = array.array('i',[0])
opflashpe = array.array('f',[0])
nvertices = array.array('i',[0])


# pot vars
pot = array.array('f',[0.0])

ttree.Branch("idx",idx,"idx/I")
ttree.Branch("run",run,"run/I")
ttree.Branch("subrun",subrun,"subrun/I")
ttree.Branch("event",event,"event/I")
ttree.Branch("opflashpe",opflashpe,"opflashpe/F")
ttree.Branch("nvertices",nvertices,"nvertices/I")

tpot.Branch("pot",pot,"pot/F")


# POT
pot[0] = 0.0
if ismc:
    for ientry in range(potchain.GetEntries()):
        potchain.GetEntry(ientry)
        pot[0] += potchain.potsummary_generator_branch.totpot
print "POT: ",pot[0]
tpot.Fill()

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
        if args.ext:
            # remove delay from EXT trigger samples (compared to BNB trigger)
            tusec -= 24*0.015625
        #print "[%d] tusec=%.2f pe=%.2f"%(iflash,tusec,flash.TotalPE())
        #if tusec>=190*0.015625 and tusec<=210*0.015625 and opflashpe[0]==0.0:
        if tusec>=3.0 and tusec<=4.9 and opflashpe[0]==0.0:
            opflashpe[0] = flash.TotalPE()

    # nvertices
    ev_pgraph = iolcv.get_data( larcv.kProductPGraph, "test" )
    nvertices[0] = ev_pgraph.PGraphArray().size()

    # Run, subrun, event, index
    run[0] = ioll.run_id()
    subrun[0] = ioll.subrun_id()
    event[0] = ioll.event_id()

    idx[0] = run[0]*10000 + event[0]

    ttree.Fill()
        
print "WRITE"
out.Write()
print "DONE"
