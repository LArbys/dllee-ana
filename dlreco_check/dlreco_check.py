import os,sys, argparse
import ROOT as rt
#from larcv import larcv
#from larlite import larlite


def load_dlmerged_file( filename, ioname ):

    iolcv = larcv.IOManager( larcv.IOManager.kREAD, 
                             "lcv_"+ioname, 
                             larcv.IOManager.kTickBackward )
    iolcv.add_in_file( filename )
    iolcv.initialize()

    ioll  = larlite.storage_manager( larlite.storage_manager.kREAD,
                                     "ll_"+ioname )
    ioll.add_in_filename( filename )
    ioll.open()

    return {"larcv":iolcv,"larlite":ioll}

def get_entry( iodict, ientry ):
    iodict["larcv"].read_entry( ientry )
    iodict["larlite"].go_to( ientry )

def get_entries( filename ):
    
    rfile = rt.TFile( filename, "READ" )
    entries = {}
    for tname in ["image2d_wire_tree","pgraph_test_tree","track_trackReco_tree","shower_showerreco_tree"]:
        tree = rfile.Get(tname)
        entries[tname] = tree.GetEntries()

    return entries

if __name__ == "__main__":

    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    ok = True    
    try:
        input_entries  = get_entries(input_file)
        output_entries = get_entries(output_file)

        print "input: ",input_entries
        print "output: ",output_entries

        base_entries = input_entries["image2d_wire_tree"]
        print "base entries: ",base_entries
        for tname in ["image2d_wire_tree","pgraph_test_tree","track_trackReco_tree","shower_showerreco_tree"]:
            if input_entries[tname]!=base_entries or input_entries[tname] != output_entries[tname] or output_entries[tname]!=base_entries:
                ok = False
                print "error in ",tname
    except:
        ok = False

    print ok
    

