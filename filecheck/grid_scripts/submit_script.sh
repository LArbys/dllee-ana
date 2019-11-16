#!/bin/bash

#SBATCH --job-name=dlsumtree
#SBATCH --output=dlsumtree.log
#SBATCH --mem-per-cpu=2000
#SBATCH --time=30:00
#SBATCH --array=0-100

CONTAINER=/cluster/tufts/wongjiradlab/larbys/larbys-containers/singularity_ubdl_deps_py2_10022019.simg
FILECHECK_DIR=/cluster/tufts/wongjiradlab/twongj01/dllee-ana/filecheck
GRID_DIR=$FILECHECK_DIR/grid_scripts

#SAMPLE=dlmergedsparsessnet_mcc9jan_extbnb
#SAMPLE=dlmergedsparsessnet_mcc9jan_bnb5e19
#SAMPLE=dlmergedsparsessnet_mcc9_v13_bnb_overlay_run1
SAMPLE=dlmergedsparsessnet_mcc9_v13_nueintrinsics_overlay_run1
#SAMPLE=dlmergedsparsessnet_mcc9_v13_overlay_dirt_run1

module load singularity
singularity exec $CONTAINER bash -c "cd $GRID_DIR && source run_script.sh $SAMPLE $GRID_DIR"
