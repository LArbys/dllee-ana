#!/bin/bash

# name a dataset/table to get files for
table=mcc9_v13_nueintrinsics_overlay_run1

mkdir -p filelists
query="SELECT run,subrun,mcinfo from ${table}_paths order by run,subrun asc"
cmdx="\x \\\\ ${query}"
echo $cmdx
#echo ${cmdx} | psql -h lnsnudot.mit.edu -U tufts-pubs procdb | grep mcinfo | awk '{print $3 }' > filelists/${table}_mcinfo.list

