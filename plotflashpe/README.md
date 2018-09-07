# PlotFlash PE

Script that gathers flash information from the tagger output for plotting

## Steps

First, get the name of the sample you want to run. For example, `mcc8v7_bnbcosmic_overlay_p01`.

* Use `pubs/dlleepubs/utils/dump_project_rse_files.py` to make a list of `supera` files for which the `tagger` PUBS completed successfully

      [go to tufts cluster]
      cd wongjiradlab/larbys/pubs
      source setup_dlleepubs_procdb.sh
      cd dlleepubs/utils
      python dump_project_rse_files.py mcc8v7_bnbcosmic_overlay tagger 4 -f supera > superalist.txt

  The last command asks for database entries where the tagger was successfully completed (status=4) for the projects coming from filetable `mcc8v7_bnbcosmic_overlay_p01`.  
  The `-f` flag tells us to return paths for `supera` files. 
  The result of the query goes into `superalist.txt`

* clean up `superalist.txt` by removing the lines that have `DEBUG` statements about the pubs database (I haven't figured out how to remove these yet).
* copy `superalist.txt` to the folder `superalists` in this repository.
* edit run_job.sh to use your supera list and set the working directory to the same as this one
* edit `run_plotflashpe.py` to run the number of `filesperjob` you want. Set to 10 currently.
* calculate number of jobs you need. get the total files by `cat superalists/[you_list.txt] | wc -l`, divide by 10 and add 1
* edit submit.sh to run those jobs by setting `#SBATCH --array=0-N` with N being number of jobs
* jaunch jobs using `sbatch submit.sh`
* once finished, will leave many files in `output` folder
* hadd them using `hadd.sh`. change file to set output and workdir. then run using `sbatch hadd.sh`

