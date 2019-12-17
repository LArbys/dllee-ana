import os,sys,argparse,json

# name a dataset/table to get files for
table="mcc9_v28_nueintrinsics_wctagger"

flistfolder="filelists"

query="SELECT t1.run,t1.subrun,t2.supera,t1.data from %s t1 join %s t2 on t1.run=t2.run and t1.subrun=t2.subrun where status=4 order by run,subrun asc"%( "dlreco_"+table, table+"_paths" )
cmdx="echo \"\\x \\\\\\\\ %s\" | psql -h lnsnudot.mit.edu -U tufts-pubs procdb" %( query )
print cmdx
pout = os.popen(cmdx)
plines = pout.readlines()


current_run = None
current_subrun = None

data = {}

for l in plines:
    l = l.strip()
    print l
    info = l.split("|")
    if len(info) and "run"==info[0].strip():
        current_run = int(info[1].strip())
    elif len(info) and "subrun"==info[0].strip():
        current_subrun = int(info[1].strip())
    if len(info)>1 and "data"==info[0].strip():
        dbdata = json.loads( info[1].strip() )
        if (current_run,current_subrun) not in data:
            data[(current_run,current_subrun)] = {}
        data[(current_run,current_subrun)]["dlreco"] = dbdata["dlreco"]

    if len(info)>1 and "supera"==info[0].strip():
        if (current_run,current_subrun) not in data:
            data[(current_run,current_subrun)] = {}
        data[(current_run,current_subrun)]["supera"] = info[1].strip()

print data

keys = data.keys()
keys.sort()

fout = open('%s/%s.list'%(flistfolder,table),'w')
for k in keys:
    print>>fout,data[k]["supera"],'\t',data[k]["dlreco"]

fout.close()

