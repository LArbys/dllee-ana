# SSNet Check

Analysis scripts to check the quality of the SSNet/Instance/Ancestor truth labels

We measure the following:

* correct pixels: ADC>threshold + label provided
* missing labels: ADC>threshold + label provided
* out-of-place labels: ADC==0 && label provided

Inputs the analysis scripts are

* the ADC image (`wire`)
* a truth label image (`ssnet`, `instance`, `ancestor`)

## Notes on the labels

### SSNet 

SSNet (`segment`) label images mark the particle type for each pixel. We mark the following:

* (code list here)

These derive from the SimChannel data. For more than one particle depositing energy
in a given pixel, the PID of the particle that makes the single largest energy deposition is used.

### Instance label

`instance` label image records the Geant4 trackid in each pixel.
These come from the TrackID saved in the SimChannel data

### Ancestor label

`ancestor` label image records the Geant4 ID number of the ancestor particle of the particle
that deposited the largest amount of energy into the pixel.
The ID of the particle that deposited the energy is recorded in SimChannels.
To get the ancestor, we need to look up information on the particle in the
MCTrack and MCShower products (which are created by MCReco).

Some tracks do not have an MCTrack and MCShower as
information from particles which deposit energy below some threshold are not saved.
These are mostly low energy photons. For pixels whose charge is due to such particles do
not have a label saved. 

