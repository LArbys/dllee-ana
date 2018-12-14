#!/bin/bash

table=mcc9tag2_nueintrinsic_corsika

query="'SELECT t1.run,t1.subrun,t1.reco2d from ${table}_paths t1 join flashmatch_${table} t2 on (t1.run=t2.run and t1.subrun=t2.subrun) where t2.status=4 order by run,subrun asc'"
#query="\"select * from ${table}_paths order by run,subrun asc\""
echo $query
cmd="psql -h nudot.lns.mit.edu -U tufts-pubs procdb -c ${query}"
echo $cmd
${cmd}