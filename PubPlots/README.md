
# Plots for Publication

The files necessary to produce plots for a PAS, publication, supplementary material, or for the technical twiki page are produced from the code in PubPlots.

```
cd PubPlots
python scripts/fill_all_inputs.py 
```

The above function will create formatted histograms for the bkg estimate, data, post-fit backgrounds, and selected signal points. The bkg and data are filled for the full Run2 data if no argument is specified or according to Run Eras (2016,2017, 2018, 2018HEM). The full Run2 background estimates are taken from the same area as for the likelihood inputs: DatacardBuilder/inputHistograms/histograms_137.4fb . The Run era inputs are in SCRA2BLE/PubPlots/inputs/ where the background estimate is only done with the data in a given run period. These inputs are included for checks and can be compared to the full Run2 background estimates. The above script makes a call to the following python scripts: fill_hadtau_hists.py,fill_znn_hists.py,fill_qcd_hists.py, and fill_data_hists.py. Each function takes the input files and creates a histogram of systematic and statistical uncertainties and projections. Search regions are integrated over accounting for bin correlations to give the correct uncertainty for the 1D and 2D projections and also the aggregate bins. The functions in fill_postfit.py do the same for the post-fit background where there is only a single post-fit uncertainty. 

```
python scripts/make_all_pas_plots_and_tables.py
``` 
The above function then plots a full suite of results for the paper (for the PAS flip the switch for isPAS which is hardcoded isPAS=False;) from the formatted histograms in the previous step. 

## Notes for updates

A few parts of the code have hard-coded file paths and variables: 
- scripts/fill_signal_hists.py defines which signal points are stored in the signal histograms, so these can limit what signal is overlayed in plots
- scripts/signal_model.py hard-codes the path to look for the signal input files
- scripts/search_bin.py hard-codes the labels for the RA2 search bins, so these would be changed for any future optimization. 
- scripts/agg_bins.py contains the definition of the aggregate bins based on the summation of the 174 search bins. 
- The bkg estimation scripts: fill_qcd_hists.py,fill_znn_hists.py, and fill_hadtau_hists.py rely on the histogram keys in the input root files to be the same as used in the Run 2 legacy analysis. If these names change, these files need to be updated so that uncertainties are properly summed accounting for correlations.

 
