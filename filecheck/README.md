# File check

Several scripts to check production quality of files.

Scripts

| script | description  |
| ------ | ------------ |
| filecheck.py       | Plot the entries per file and POT per file for MC samples. |
| summary_tree.py    | Make tree of reco quantities versus run,subrun,event using dlmerged files.     |

## How to run

First, pick a data set. Lists of datasets can be found in the [Tufts PUBS monitor](http://lnsnudot.mit.edu/taritree/dlleepubsummary.html).

Next, Go to `/cluster/tufts/wongjiradlab/larbys/pubs/` and setup pubs using

     source setup_dlleepubs_procdb.sh


Then choose the script to run depending on the file type of interest.

* Use `get_mcinfo_filelist.sh` to get the `mcinfo` files for a dataset.
* Use `get_dlmerged_filelist.py` to get the list of good `dlmerged` files.




