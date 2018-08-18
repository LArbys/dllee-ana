#!/bin/bash

CONTAINER=/cluster/tufts/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20180816.img

module load singularity
singularity shell ${CONTAINER}