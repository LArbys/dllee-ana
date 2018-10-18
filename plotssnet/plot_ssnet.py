import os,sys

## ==============================================
## plot_ssnet
##
## goal is to simply make distributions
## of ssnet information for study/comparisons
##
## ==============================================

import ROOT as rt
from larcv import larcv

larcv_ssnetfile = sys.argv[1]
larcv_supera    = sys.argv[2]
out_filename    = sys.argv[3]

io = larcv.IOManager(larcv.IOManager.kREAD)
io.add_in_file( larcv_ssnetfile )
io.add_in_file( larcv_supera )
io.initialize()

tfile = rt.TFile(out_filename,"new")

# histograms of score values!

hshower_v = [ rt.TH1D("hshower_p%d"%(x),"shower scores plane %d"%(x),100,0,1.0) for x in xrange(3) ]
htrack_v  = [ rt.TH1D("htrack_p%d"%(x), "track scores plane %d"%(x), 100,0,1.0) for x in xrange(3) ]

for i in xrange(io.get_n_entries()):
    io.read_entry(i)

    print "Entry %d"%(i)
    
    ev_ssnetout_planes = [ io.get_data( larcv.kProductImage2D, "uburn_plane%d"%(x) ) for x in xrange(3) ]
    ev_img = io.get_data( larcv.kProductImage2D, "wire" )
    for p in xrange(3):
        if ev_ssnetout_planes[p].Image2DArray().size()==0:
            continue
        showerimg = ev_ssnetout_planes[p].Image2DArray().at(0)
        trackimg  = ev_ssnetout_planes[p].Image2DArray().at(1)
        adcimg = ev_img.Image2DArray().at(p)
        meta = showerimg.meta()
        for r in xrange( meta.rows() ):
            for c in xrange( meta.cols() ):

                try:
                    t = meta.pos_y( r ) # convert
                    w = meta.pos_x( c )
                    val = adcimg.pixel( adcimg.meta().row(t), adcimg.meta().col(w) )
                    if val>10.0:
                        #print "above thresh pixel",val," ",showerimg.pixel(r,c)
                        hshower_v[p].Fill( showerimg.pixel(r,c) )
                        htrack_v[p].Fill( trackimg.pixel(r,c) )
                except:
                    print "error acessing (%d,%d)"%(r,c)
    sys.stdout.flush()

tfile.Write()

    





