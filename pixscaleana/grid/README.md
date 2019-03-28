Instructions

* first build the program `run_pixscale_ana.cxx` (one folder up)
* use `get_filelist.sh` (also in one folder up) to make list of files. you need the list of supera files for a given PUBs dataset
* generate the job tracking files by editing `check_jobs.py` to read in your filelist and then running 

      source run_check_jobs.sh

  which will run `check_jobs.py` in a container.
*  use `tufts_submit_pixscanana.sh` to submit jobs
* after jobs are finished, run `source run_check_jobs.sh` 
  which updates the rerun list (`rerun_processing.list`) and 
  also provides jobid for failures (`err_processing.list`). 
  Successful jobs are in `processedok.list`
* repeat until all jobs are processed