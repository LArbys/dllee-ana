# DLRECO Check

This is used to 

* double check the quality of the output files from the dlreco.
* provide a paired list of input and output files for output files that are checked as good.

The output files are checked by seeing if the following trees have the same number of entries 
as the same trees in the input files. If the trees are missing, the files are also marked bad.

* image2d_wire_tree: the ADC image
* pgraph_test_tree: the output of the vertexer
* track_trackReco_tree: the output of the tracker
* shower_showerreco_tree: output of the shower reco

# Workflow

* pick you data sample and set it in `get_dlmerged_filelist.py`.
* get a list of input and output files from the PUBs database where the jobs were marked as good (status=4)

       python get_dlmerged_filelist.py

  This will make a file list in the `filelists` folder with the name of your sample.
* Set the filelist you want to check over in `run_checklist.sh`.
* give the file to the checking script.

    `source run_checklist.sh`


The output will be a good and bad file list. The good list will contain a pair of files (`"input" "output"`) in each line.

