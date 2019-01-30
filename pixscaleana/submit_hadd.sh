#!/bin/bash
#
#SBATCH --job-name=hadd_plotssnet
#SBATCH --output=log_hadd_plotssnet
#SBATCH --mem-per-cpu=2000
#SBATCH --time=1-00:00:00


CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-unified-ubuntu16.04-20181010-mcc9beta1.img
WORKDIR_IC=/cluster/kappa/wongjiradlab/twongj01/dllee-ana/pixscaleana

sample="mcc9tag2_nueintrinsic_corsika"
#sample="mcc9tag1_bnb5e19"
#sample="mcc8v6_extbnb"
#sample="mcc9_extbnb_beta1"
#sample="mcc8v11_bnbcosmic_detsys_cv"

module load singularity
singularity exec ${CONTAINER} bash -c "cd /usr/local/share/dllee_unified && source configure.sh && cd ${WORKDIR_IC} && hadd -f output_${sample}.root output/${sample}/*.root"