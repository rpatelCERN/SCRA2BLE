# Public Plots
This directory contains the scripts used to make the public plots included in CMS-PAS-SUS-16-014 and the supplementary material.

## Overview

The [inputs](./inputs/) directory contains root files containing the 160-bin histograms of the observed data, data-driven background estimates and their uncertainties, and the expected contribution from various signal models. The [scripts](./scripts/) directory contains all of the code needed to produce the plots. All scripts are intended to be run from the [PubPlots](./) directory. All plots and tables produced by these scripts should be written to the [output](./output/) directory. Reference copies of the plots and tables made for our ICHEP result are included [here](./output/reference/).

Any new aggregate search regions or sets (histograms) of aggregate search regions should be added to [agg_bins.py](./scripts/), following the examples provided. Any new correlation model (e.g. correlating over the 'nbjets' dimension) should be added to [uncertainty.py](./scripts/uncertainty.py#L46) following the examples provided.

## Instructions

### Setup
This code should run on a system with Python >= 2.7 and ROOT 6.

```
git clone git@github.com:nhanvtran/SCRA2BLE -b ICHEP2016
cd SCRA2BLE/PubPlots
```

### Produce input histograms
These scripts will make all histograms and calculate relevant uncertainties for each of the backgrounds, the observed data, and several signal models and save them to ROOT files that will be loaded in the next step. This step also handles the combination of bins for aggregate search regions (including 1-D projections), as well as the (almost) full correlations between background systematics.



