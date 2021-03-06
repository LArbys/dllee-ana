#!/bin/bash

CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20181010-mcc9beta1.img
WORKDIR_IC=/cluster/kappa/wongjiradlab/twongj01/dllee-ana/plotssnet/

sample="mcc9tag2_nueintrinsic_corsika"
#sample="mcc9tag1_bnb5e19"
#sample="mcc8v6_extbnb"
#sample="mcc9_extbnb_beta1"
#sample="mcc8v11_bnbcosmic_detsys_cv"

module load singularity
singularity exec ${CONTAINER} bash -c "cd ${WORKDIR_IC} && source setup_container.sh && hadd -f output_${sample}.root output/${sample}/*.root"