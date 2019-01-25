#/bin/bash

samplefile=$1
runtable="mcc9tag2_nueintrinsic_corsika"

# first split the sample into different files

cat $samplefile | awk '{ print $1 }' > tmp_dlvertex.list
cat $samplefile | awk '{ print $2 }' > tmp_classic.list

# merge
#cat tmp_dlvertex.list tmp_classic.list > tmp_merged_xfer.list

# truncate (for debug)
#head -n 3 tmp_merged_xfer.list > tmp_merged_xfer_truncated.list
#mv tmp_merged_xfer_truncated.list tmp_merged_xfer.list

# transfer dlvertex
mkdir -p data/${runtable}/dlvertex
rsync -av --progress --no-relative --files-from=tmp_dlvertex.list twongj01@xfer.cluster.tufts.edu:/ data/${runtable}/dlvertex/

# transfer classic
mkdir -p data/${runtable}/classic
rsync -av --progress --no-relative --files-from=tmp_classic.list twongj01@xfer.cluster.tufts.edu:/ data/${runtable}/classic/

# clean up tmp files
rm tmp_*.list
