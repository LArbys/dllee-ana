#!/bin/bash

CONTAINER=/cluster/tufts/wongjiradlab/larbys/larbys-containers/singularity_ubdl_deps_py2_091319.simg


SETUP="source /usr/local/root/root-6.16.00/bin/thisroot.sh && \
source /cluster/tufts/wongjiradlab/twongj01/dev/ubdl/setenv.sh && \
source /cluster/tufts/wongjiradlab/twongj01/dev/ubdl/configure.sh"

singularity exec $CONTAINER bash -c "$SETUP && python filecheck.py"