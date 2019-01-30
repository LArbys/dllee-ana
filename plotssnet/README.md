# Plot SSNet

SSNet analysis scripts


# Instructions

## Building

First, setup your copy of LArCV (or dllee_unified) by running their respective configure scripts.

Then return this folder and run 'make'.

In principle it should build.

## Running

These scripts were designed to be run on the Tufts grid.
We use the Tufts PUBs database to provide us with a set of input files to run.
We process each file one-by-one, but process many at once using the Tufts grid.

The following are the steps to go from filelist (from PUBs), to output TROOT file.

### Step 1: Get the filelist

* First, remember to setup the environment for the PUBs production database. 
  (`source setup_dlleepubs_procdb.sh` in the Tufts PUBs folder.)

* Next, use `get_filelist.sh` to generate a list of files that have been processed successfully by `serverssnetv2`.

* Go into `get_filelist.sh` and set the name of the file table (e.g. mcc9tag2_nueintrinsic_corsika).

* `source get_filelist.sh`: as a result you should see a list of files in `filelist/${table}_ssnet.list` (and one for supera files.)

### Step 2: compile the script

* For the Tufts grid, we provide script to submit a job for compiling the code. 
  It basically loads a singularity container containing a copy of `dllee_unified`, sets it up, then runs make

      source compile.sh

### Step 3: launch the jobs

* Go into `submit.sh` and change the `TAG` variable to reflect the file table name used for the sample.
* Still inside `submit.sh`, adjust the number of jobs (and which subset of the files) to run using the `--array` flasg
* LAUNCH
     sbatch submit.sh

### Step 4: hadd

* The files automatically stored in `output/${tagname}/`.   
* To merge them into one file for convience using `hadd.sh`.
* Go to `hadd.sh` and change the table name (tag name)
* source hadd.sh (if the number of files are not crazy large)

## To do for scripts

(to do)



