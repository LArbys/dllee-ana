import os,sys

from goodfilelist import get_vertexana_list

if __name__ == "__main__":
    """ we get the overlapping sample between dlcosmic and classic vertex projects"""

    runtable = "mcc9tag2_nueintrinsic_corsika"
    
    classic  = get_vertexana_list( runtable, "vertex" )
    dlvertex = get_vertexana_list( runtable, "dlcosmicvertex" )

    keylist = dlvertex.keys()
    keylist.sort()

    # write filelist for overlapping sample
    fout = open("inputlists/%s_overlapsample.list"%(runtable),'w')
    noverlap = 0
    for key in keylist:
        if key in classic:
            print >>fout,"{} {}".format( dlvertex[key], classic[key] )
            noverlap += 1
    fout.close()

    print "found ",noverlap," overlap files"
            

    
