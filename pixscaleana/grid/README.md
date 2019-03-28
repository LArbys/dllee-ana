Instructions

The scripts here are intended to process files stored in the PUBs database.
We get a list of files from the PUBs DB and then process each using the cluster.

We process each file through the program `run_pixscale_ana` found one folder above this one.

Before using these scripts, this program must be build. It is intended to link against a 
working copy of the `UBDL` repository of repositories which contains the software tools
we use to analyze the MicroBooNE data files. Specifically the `LArCV` library 
(for files containing images for each MicroBooNE event)
and `larlite` library (for files containing meta-data for each event, e.g. truth
information about the particles in the images, details about the data such as time of event,
or optical information recorded in-time with the event.)

We use a container with UBDL already built, so we compile within the container.

* first build the program `run_pixscale_ana.cxx` (one folder up. see instructions there.) 
* use `get_filelist.sh` (also in one folder up) to make list of files. 
  you need the list of supera files for a given PUBs dataset. 
  in the script you need to specify the "table" name for the sample.
* generate the job tracking files by editing `check_jobs.py` to read in your filelist and then running 

      source run_check_jobs.sh

  which will run `check_jobs.py` in a container.
*  use `tufts_submit_pixscanana.sh` to submit jobs
* after jobs are finished, run `source run_check_jobs.sh` 
  which updates the rerun list (`rerun_processing.list`) and 
  also provides jobid for failures (`err_processing.list`). 
  Successful jobs are in `processedok.list`
* repeat until all jobs are processed
* finally, once all (or enough) jobs are complete, run hadd to merge the files

      sbatch submit_hadd.sh

