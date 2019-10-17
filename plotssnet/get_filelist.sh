#!/bin/bash

#table=mcc9jan_extbnb
table=mcc9_v13_bnbnue_corsika

query="SELECT t1.run,t1.subrun,t1.supera from ${table}_paths t1 join sparsessnet_${table} t2 on (t1.run=t2.run and t1.subrun=t2.subrun) where t2.status=4 order by t1.run,t1.subrun asc"

sedreplace1=`printf 's|supera|sparsessnet-larcv-%s|' ${table}`
mkdir -p filelists
cmdx="\x \\\\ ${query}"
echo ${cmdx} | psql -h lnsnudot.mit.edu -U tufts-pubs procdb | grep supera | awk '{ print $3 }' > filelists/${table}_supera.list
echo ${cmdx} | psql -h lnsnudot.mit.edu -U tufts-pubs procdb | grep supera | awk '{ print $3 }' | sed $sedreplace1 | sed 's|/stage1|/sparsessnet/v0_0_2|' > filelists/${table}_ssnet.list
