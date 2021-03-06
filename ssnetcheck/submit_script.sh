#!/bin/bash

#SBATCH --job-name=check-ssnet
#SBATCH --output=/cluster/tufts/wongjiradlab/twongj01/dllee-ana/ssnetcheck/logs/check.log
#SBATCH --mem-per-cpu=2000
#SBATCH --time=10:00
#SBATCH --array=600-799

CONTAINER=/cluster/tufts/wongjiradlab/larbys/larbys-containers/singularity_ubdl_deps_py2_091319.simg
SSNET_CHECK_DIR=/cluster/tufts/wongjiradlab/twongj01/dllee-ana/ssnetcheck/

#INPUTLIST=$SSNET_CHECK_DIR/inputlists/supera_list_mcc9_v13_nueintrinsics_overlay_run1_good_ssnetserver_files.txt
#INPUTLIST=$SSNET_CHECK_DIR//inputlists/supera_list_mcc9jan_extbnb_good_ssnetserver_files.txt
#INPUTLIST=$SSNET_CHECK_DIR/rerunlists/rerun_supera_list_mcc9jan_extbnb_good_ssnetserver_files.txt
#INPUTLIST=$SSNET_CHECK_DIR/inputlists/supera_list_mcc9jan_bnb5e19_good_ssnetserver_files.txt
INPUTLIST=$SSNET_CHECK_DIR/inputlists/supera_list_mcc9_v13_bnb_overlay_run1_good_ssnetserver_files.txt
OUT_FILE_DIR=$SSNET_CHECK_DIR/resultfiles/

module load singularity
singularity exec $CONTAINER bash -c "cd $SSNET_CHECK_DIR && source run_script.sh $INPUTLIST $OUT_FILE_DIR $SSNET_CHECK_DIR"