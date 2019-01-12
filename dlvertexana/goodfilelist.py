#!/bin/usr/env python
import os,sys

PUBS_DIR="/cluster/tufts/wongjiradlab/larbys/pubs"
WORKDIR=os.environ["PWD"]

def get_vertexana_list( runtable, project ):
    """ remember to setup pubs
    cd $PUBS_DIR
    source setup_dlleepubs_procdb.sh
    """
    # dump the good entries and get the supera file path
    plist = os.popen("python {}/dlleepubs/utils/dump_project_rse_and_files.py {} {} 4 -f supera".format(PUBS_DIR,runtable,project))
    plines = plist.readlines()

    # parse list
    vertexana_list = {}
    for l in plines:
        l = l.strip()
        if ".root" not in l:
            continue
        f = l.split(' ')[2]
        run    = int(l.split(' ')[0])
        subrun = int(l.split(' ')[1])
        jobnum = run*10000 + subrun
        if project=="vertex":
            # classic
            fname = os.path.dirname(f.replace("stage1","stage2/test21")) + "/vertexana_%d.root"%(jobnum)
        elif project=="dlcosmicvertex":
            fname = f.replace("stage1","dlcosmicvertex").replace("supera","dlcosmicvertex-ana")
        else:
            raise ValueError("unrecognized project {}".format(project))
        vertexana_list[(run,subrun)] = fname

    print "Found ",len(vertexana_list)," files"
    return vertexana_list

def write_list( runtable, project ):
    keylist = vertexana_list.keys()
    keylist.sort()
    fout = open("inputlists/%s_%s_vertexana.list"%(runtable,project),'w')
    
    for (run,subrun) in keylist:
        print >> fout, vertexana_list[(run,subrun)].strip()

    fout.close()


if __name__ == "__main__":
    """main"""
    # runtable = sys.argv[1]
    # project  = sys.argv[2]

    runtable="mcc9tag2_nueintrinsic_corsika"
    project="vertex"

    vertexana_list = get_vertexana_list( runtable, project )
    write_list( runtable, project )

    



