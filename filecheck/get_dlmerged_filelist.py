import os,sys,argparse,json

# name a dataset/table to get files for
#table="dlmergedsparsessnet_mcc9jan_extbnb"
#table="dlmergedsparsessnet_mcc9jan_bnb5e19"
#table="dlmergedsparsessnet_mcc9_v13_bnb_overlay_run1"
table="dlmergedsparsessnet_mcc9_v13_nueintrinsics_overlay_run1"
#table="dlmergedsparsessnet_mcc9_v13_overlay_dirt_run1"

flistfolder="filelists"

query="SELECT run,subrun,data from %s where status=4 order by run,subrun asc"%( table )
cmdx="echo \"\\x \\\\\\\\ %s\" | psql -h lnsnudot.mit.edu -U tufts-pubs procdb" %( query )
print cmdx
pout = os.popen(cmdx)
plines = pout.readlines()

fout = open('%s/%s.list'%(flistfolder,table),'w')
for l in plines:
    l = l.strip()
    info = l.split("|")
    if len(info)>1 and "data"==info[0].strip():
        #print info[1]
        dbdata = json.loads( info[1].strip() )
        print>>fout,dbdata["dlmerged"]

fout.close()

