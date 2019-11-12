import os,sys,argparse,json

# name a dataset/table to get files for
#sample="mcc9jan_extbnb"
#sample="mcc9jan_bnb5e19"
sample="mcc9_v13_bnb_overlay_run1"

flistfolder="filelists"

query ="SELECT t1.run,t1.subrun,pathtable.superasam"
query+=" from dlmergedsparsessnet_%s t1 join %s_paths pathtable on (t1.run=pathtable.run and t1.subrun=pathtable.subrun)"%(sample,sample)
query+=" where status=4 order by t1.run,t1.subrun asc"
cmdx="echo \"\\x \\\\\\\\ %s\" | psql -h lnsnudot.mit.edu -U tufts-pubs procdb" %( query )
print cmdx
pout = os.popen(cmdx)
plines = pout.readlines()

fout = open('%s/%s.list'%(flistfolder,sample),'w')
for l in plines:
    l = l.strip()
    info = l.split("|")

    if len(info)>1 and "superasam"==info[0].strip():
        print>>fout,info[1].strip()

fout.close()

