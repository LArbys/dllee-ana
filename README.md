# dllee-ana

Repository to hold a number of quick analysis scripts that extract data from files produced by DLLEE PUBS.

Contents

## skim_mctruth

Takes in larlite `mcinfo` file and provides flat ROOT ntuple that contains basic MC truth information for the event.
Can serve as an example of how to reduce larlite/larcv data into analysis ntuple.

The repo has the following basic components:

* GNUmakefile to compile and build a basic program 
* Example of opening a larlite file and accessing data products
* Navigation of the truth information data types: `mctruth`, `mcshower`, 'mcreco`
* Compiling the code within a container
* Running the code within a container
* Creating a list of files to run on by accessing the PUBS database
* Launching an array of jobs on the cluster
* Merging the output
* A simple analysis of the data using pandas
* plotting example
