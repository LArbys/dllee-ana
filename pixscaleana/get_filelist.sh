#!/bin/bash

#table=mcc9tag2_nueintrinsic_corsika
#table=mcc9tag1_bnb5e19
table=bnbcosmic_detsys_cv

query="SELECT t1.run,t1.subrun,t1.supera,t1.reco2d from ${table}_paths t1 join xferinput_${table} t2 on (t1.run=t2.run and t1.subrun=t2.subrun) where t2.status=3 order by t1.run,t1.subrun asc"

mkdir -p filelists
cmdx="\x \\\\ ${query}"
echo ${cmdx} | psql -h nudot.lns.mit.edu -U tufts-pubs procdb | grep supera | awk '{ print $3 }' > filelists/flist_supera_${table}.list
echo ${cmdx} | psql -h nudot.lns.mit.edu -U tufts-pubs procdb | grep reco2d | awk '{ print $3 }' > filelists/flist_reco2d_${table}.list