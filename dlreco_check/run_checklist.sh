#!/bin/bash

module load singularity

CONTAINER=/cluster/tufts/wongjiradlab/larbys/larbys-containers/singularity_ubdl_deps_py2_10022019.simg

singularity exec $CONTAINER bash -c "source /usr/local/root/root-6.16.00/bin/thisroot.sh && python run_checklist.py filelists/mcc9_v28_nueintrinsics_wctagger.list"