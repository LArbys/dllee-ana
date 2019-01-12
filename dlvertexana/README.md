# Vertex Ana

This code is used to analyze the results of the LArOpenCV vertex reconstruction

## Summary of workflow

One should setup the shell to be able to query the Tufts PUBS database. 
Use `setup_tufts_pubs.sh`.

* Process sample through PUBS `vertex` or `dlcosmicvertex` stage
* Get list of entries that produced a good file using `goodfilelist.py` script
* We need `mcskim` files (produced using the `skim_mctruth`) that cover the same (run,subrun,event) range as the vertex files
* We use a `pandas` analysis to calculate and plot various quantities

We also want to compare the vertex code event-by-event.  We can define a comparison sample using `comparisonlist.py`.


