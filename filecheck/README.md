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


# Checking file quality and making check of variables over Run index

The steps involved

## 1) make a file list

Edit `get_dlmerged_filelist.py` and set the sample to be checked.

Then run the script

    python get_dlmerged_filelist.py

You should see a text file in the `filelists` folder with the sample name in the title. 
It should have the paths for the dlmerged files on the Tufts cluster.

## 2) Count the number of files

    cat filelists/dlmergedsparsessnet_[sample].list | wc -l


Jot this number down.

## 3) submit a job that runs `summary_tree.py` for all files

Go to the `grid_scripts` folder. Edit `submit_script.sh` to use your sample.

Also edit the number of jobs to run. 
This should be the number of files in the filelist/10.
Then set the jobs to run using the `--array` argument found in the top portion of `submit_script.sh`.
Should look like 

    --array=0-99

if you have 100 jobs.

## 4) launch jobs

    sbatch submit_script.sh

## 5) make a list of good files

    find . -name "output_*.root" | sort > goodlist.txt

## 6) hadd 

    hadd -f myoutput.root @goodlist.txt

Below are Optional

## 7) compile list of bad files

    find . -name "bad_dlmerged_list.txt" | xargs cat | sort > badlist.txt

## 8) update the database by reseting job status for bad (run,subruns)

BE VERY CAREFUL ABOUT THIS NEXT STEP. THIS CHANGES THE PUBS DATABASE. MISTAKES COULD BE COSTLY.

If you are not sure, contact Taritree first.

First, change badlist file name and change sample name.

Then run the script.

    python reset_badlist_jobs.py


   



