# skim_mctruth

Any analysis needs to refer to truth information, in order to understand efficiencies, etc.

We produce flat ntuples from the mcinfo files of the database. The intention is to use
these in analysis script that use pandas (through root_pandas, uproot, whatever).

## Steps

* Produce list of files using the query found in get_filelist.sh. (Note, call from bash doesn't work for some reason,
  but if one types in query directly into shell, then works.
* Take the list of files and pipe it into a file. Put that file into the `inputlists` directory
* Make a copy of the list and put it into the `rerunlists` directory.
* Modify `submit_job.sh` to refer to the location of the repo, the rerun list, and the output directory
* Launch jobs. Change the `array` parameter to send the right amount.
* Use `check_files.sh` to check to see if the output exists and to reduce the number in the rerun list.
* Repeat the last three steps until all the files are processed.

