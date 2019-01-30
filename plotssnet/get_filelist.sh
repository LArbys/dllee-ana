#!/bin/bash

table=mcc9tag2_nueintrinsic_corsika
#table=mcc9tag1_bnb5e19
#table=mcc8v11_bnbcosmic_detsys_cv

query="SELECT t1.run,t1.subrun,t1.supera from ${table}_paths t1 join serverssnetv2_${table} t2 on (t1.run=t2.run and t1.subrun=t2.subrun) where t2.status=4 order by t1.run,t1.subrun asc"

mkdir -p filelists
cmdx="\x \\\\ ${query}"
echo ${cmdx} | psql -h nudot.lns.mit.edu -U tufts-pubs procdb | grep supera | awk '{ print $3 }' > filelists/${table}_supera.list
echo ${cmdx} | psql -h nudot.lns.mit.edu -U tufts-pubs procdb | grep supera | awk '{ print $3 }' | sed 's/supera/ssnetserveroutv2-larcv/' > filelists/${table}_ssnet.list