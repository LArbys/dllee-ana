import os,sys
import ROOT as rt
#from larcv import larcv

def checkfile( filepath ):
    # single-flow: Y2U
    t = rt.TChain("pixamp")

    t.Add(filepath)
    nentries = t.GetEntries()
    if nentries<=0:
        return False
    return True


if __name__ == "__main__":

    outdir  = "/cluster/tufts/wongjiradlab/twongj01/dllee-ana/pixscaleana/grid/workdir"
    folders = os.listdir(outdir)

    inputlistname = "../filelists/flist_supera_mcc8v11_bnbcosmic_detsys_cv.list"
    inputfile = open(inputlistname,'r')
    inputlist = inputfile.readlines()
    
    oklistname = "processedok.list"
    oklist = open(oklistname,'w')

    errlistname = "err_processing.list"
    errlist = open(errlistname,'w')

    rerunlistname = "rerun_processing.list"
    rerunlist = open(rerunlistname,'w')
    
    for ijob,larcvname in enumerate(inputlist):
        larcvname = larcvname.strip()
        workdir=outdir+"/jobid%04d"%(ijob)
        histout = os.path.basename( larcvname ).replace("supera","pixscaleana")
        histpath = workdir + "/" + histout
        
        if not os.path.exists(histpath):
            print histpath," does not exist"
            print >> rerunlist,ijob,larcvname.strip()
            continue
            
        ok = checkfile(histpath)

        if ok:
            print "ok=",ok," : ",histpath
            print >> oklist,histpath.strip()
        else:
            print >> errlist,histpath.strip()
            print >> rerunlist,ijob,larcvname.strip()
                
