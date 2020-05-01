# auxillary data preparation

Besides the final ntuples from the MC and data samples, there are
some auxillarity information that needs to be combined with the main data stream.

* beam quality data
* MC CV weights

The scripts in this folder are meant to extract the above info into trees that can be combined with the main data stream.

# MC Weights

Use `make_mc_cv_weight_tree.py` to make the mc weights for each MC sample. You need
the sample finalvertexvariable tree and the MC weight files.

The MC weight files are located at FNAL at:

```
/uboone/data/users/yatesla/othersys_mcc9/for_weights/
```

Contents of the folder:
```
[ tmw@uboonebuild02 Linux64bit+3.10-2.17_e17_prof ]$ ls -lh /uboone/data/users/yatesla/othersys_mcc9/for_weights/
total 98M
drwxr-xr-x 2 yatesla microboone 2.0K Mar 25 19:48 arxiv
-rw-r--r-- 1 yatesla microboone  36M Mar 25 16:51 weights_forCV_v40_bnb_nu_run1.root
-rw-r--r-- 1 yatesla microboone  40M Apr  3 16:11 weights_forCV_v40_bnb_nu_run3.root
-rw-r--r-- 1 yatesla microboone 3.5M Mar 25 19:37 weights_forCV_v40_dirt_nu_run1.root
-rw-r--r-- 1 yatesla microboone 4.1M Apr  3 16:06 weights_forCV_v40_dirt_nu_run3.root
-rw-r--r-- 1 yatesla microboone 7.3M Mar 25 16:54 weights_forCV_v40_intrinsic_nue_run1.root
-rw-r--r-- 1 yatesla microboone 7.7M Apr  3 16:09 weights_forCV_v40_intrinsic_nue_run3.root
```

# Data beam quality flag

To do.


