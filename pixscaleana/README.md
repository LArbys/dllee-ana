# PixelScale Ana

The scripts here are used to set the pixelscale.  
We use the gaus hits to define the location of peaks.
The values at those peaks are histogrammed.
The assumption is those peaks will on average be for cosmic MIP depositions.
We can use that to compare across samples and adjust the amplitude.
Normalizing the amplitude is needed to make sure that the SSNet behavior is similar as possible between samples.

The pixel scale analysis code is located in the dllee_unified repository under 

    larlitecv/app/AnalyzeTagger/run_pixelscale_analysis.cxx


## Running the analysis on a Tufts PUBS dataset

For each entry in the Tufts PUBS db, we want to provide

  * larcv1 file (supera)
  * reco2d file

To do this, we make filelists for the supera and reco2d files.

For a given sample, change the tag line in `get_filelist.sh` and then run it with

    ./get_filelist.sh

The script queries the list of super and reco2d files for entries where the `xferinput` job completes successfully.

Next, one can then change the tab in `submit.sh` and, in principle, run jobs on the grid with

    sbatch submit.sh  


To adjust the number of jobs run, modify the `array` variable in `submit.sh`.

The output of `run_pixelscale_analysis` is put into `output/[SAMPLE TAG]/`.

Next, one probably wants to `hadd` the files for convenience.

Modify `submit_hadd.sh` to use the desired sample and run (on a batch node) using

    sbatch submit_hadd.sh

You can also run it interactively with

    ./submit_hadd.sh