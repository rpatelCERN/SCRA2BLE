# SCRA2BLE

The RA2 SCRA2BLE integration code is designed to perform the necessary steps to produce the results, diagnostics,and statistical 
interpretations by combining the latest version of the background estimates into a figure or into a likelihood model. The two folders in this repository split the code into these two main functions: plotting integration results  (PubPlots) and performing likelihood fitting or diagonostics (DatacardBuilder). 

The current version of the code is based on the legacy 13 TeV [RA2 analysis](https://arxiv.org/abs/1908.04722), which 
used 174 search bins with seperate background inputs for each Run era based on the data taking periods in 2016, 2017, 2018 
(further split by HEM affected runs). The analysis used the RA2 production from the [Treemaker](https://github.com/TreeMaker/TreeMaker/tree/Run2_2017) and the signal histograms from the V17 signal samples. 

## Setup 

This was the release used for the Legacy analysis:
```	
cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src 
```	
Include the Higgs combine tool code and compile:
```
git -b 81x-root606 clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v7.0.9
scramv1 b clean; scramv1 b  
```

Note that future versions of the analysis the combine tool recipe would be updated for new CMSSW releases like (e.g. 10X and beyond). Find the latest instructions on the [CombineToolTwiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit). 

Also in order to complete the full set of [pre-approval checks](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSPAGPreapprovalChecks) it is also necessary to use the [CombineHarvester](http://cms-analysis.github.io/CombineHarvester/) in order to compute the impact of each nuisance parameter.

```
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
```


```
git clone -b Run2LegacyPub  https://github.com/rpatelCERN/SCRA2BLE.git
```

## Building DataCards for the Combine Tool

The python scripts in DatacardBuilder are designed to take the input bkg estimate histograms as well as an input SMS fastSIM signal point and create datacards for the combine tool.
The code is in analysisBuilderCondor.py, and includes various options to call methods in the Higgs Combine tool. The scripts also include plotting code for the 2D interpretations,
which include the cross-section UL, signal significance, and signal efficiency. An example command is shown below for a single signal point:

```
python analysisBuilderCondor.py --signal T1bbbb --mGo 1500 --mLSP 100 --fastsim --realData --CombOpt=AsymptoticUL
```

The options specified for the signal point: 

```
--signal T1bbbb --mGo 1500 --mLSP 100 
```

bool options below specify that the input signal is fastsim (as opposed to FullSIM) and to use the unblinded data for the observation (otherwise use the sum of the total bkg)

```
--fastsim --realData
```

The last option specifies which method to run in the combine code: 

```
--CombOpt=AsymptoticUL #(or MaxLiklihood, Significance, FitCovariance, ImpactsInitialFit)
```

The option for AsymptoticUL just runs the Asymptotic upper limits. The other options call different combine methods: 
- MaxLiklihood computes the post-fit background yields which are input to the plotting code in the next section
- Fit Covaraince performs the maxlikelihood fit and throws toys to compute the covariance matrix
- ImpactsInitialFit calls the Combine Harvester tool to fit the likelhood and nuisances (need this is the right format to compute the nuisance impacts)
- The Significance calls the ProfileLikelihood method to compute the observed significance
### Preapproval Checks

A number of the [pre-approval checks](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSPAGPreapprovalChecks) can be done with the MaxLiklihood option using analysisBuilderCondor.py. (Use the modifications recommended in the page to toggle between the expectSignal=0, 1 hypotheses). The output results of the MaxLiklihood fit can be plotted and examined using 
```
python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py 
```
The above code provides either a table or a plot (specified by the options) can be used to test the behavior of certain nuisance parameters. We expect correlations in the background uncertainty to shrink the uncertainty on a nuisance parameter after the fit. 

The nuisance impacts can be computationally intensive due to the large number of nuisance parameters in the RA2 likelihood model. It is useful then to break up the impacts into jobs per background estimate or signal in the last step: QCD, Zvv, Lost-lepton, and signal. The procedure for computing Impacts is shown on this twiki:[Nuisance_parameter_impacts](https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/SWGuideNonStandardCombineUses#Nuisance_parameter_impacts)
The steps below show how to produce an impact plot for a subset of nuisances using the RA2 code:
1. Derive the initial fit to the likelihood using the command for analysisBuilderCondor.py --CombOpt=ImpactsInitialFit. This will produce a file: higgsCombine_initialFit_Test.MultiDimFit.mH125.root
This will be used for plotting the fitted mu and uncertainty and to find the fitted nuisance parameters
2. Fit each nuisance parameter as POI. It would take a long time to fit all of them, so in the script QuickNuisnce.py I show how you can run over subsets in batch jobs (the script uses the CU cluster with the Qsub command but it could be adapted to other clusters or the LPC).
3. Create a Json of all the fitted parameters and their uncertainties. 
4. Read in the JSON and produce the impacts plot

The full set of commands is shown for an example signal point here:

```
python analysisBuilderCondor.py --signal T1tttt --mGo 950 --mLSP 700 --fastsim --realData --eos root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/ --CombOpt=ImpactsInitialFit

combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0 -n _paramFit_Test_zvvgJNobs_NJets4_MHT1_HT4 --rMin=-10 --rMax=10 --algo impact --redefineSignalPOIs r -P zvvgJNobs_NJets4_MHT1_HT4 --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_950_700-137.4/allcards.root
####Sumbit to batch as: python QuickNuisnce.py testCards-Moriond-T1tttt_950_700-137.4

combineTool.py -M Impacts -d testCards-Moriond-T1tttt_950_700-137.4/allcards.root -m 125 -o impacts.json
plotImpacts.py -i impacts.json -o impacts
```
The results in an impacts plot stored in impacts.pdf

### Covariance /Correlation Matrices
This matrix is generated using the FitCovariance option for analysisBuilderCondor.py which gives an output file like: fitDiagnosticstestCards-Moriond-XXXX.root (XXXX=output directory name)
The covariance matrix is already stored in shapes_prefit/overall_total_covar. 

The Covariance matrix can be checked and also used to create the correlation matrix using: plottingStuff/QuickCovarianceFormat.C . This code orders the covariance matrix according to bin number, cross-checks the diagonal against the known pre-fit uncertainties from the inputs (store these in PrefitUnc.root), and computes a correlation matrix. 
The matrices are plotted with plottingStuff/QuickCovariancePASPlot.C 

```
cd plottingStuff
root -b 'QuickCovarianceFormat.C(fname)'
root -b 'QuickCovariancePASPlot.C'  
```

### Submitting Jobs
A single python script is used to run a 2D scan for a signal sample for the two main cases: Upper Limits and significance
```
python launchSCRA2BLE.py --fastsim --model=T1tttt --keeptar --lpc --CombOpt AsymptoticUL --inDir /store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/ --outDir=/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/
```

The python script runs by default on the lpc but can be modified to run on other clusters. The flag --lpc uses the mode that submits jobs to LPC condor. 
The code tars the CMSSW area and creates a condor submission area in a new directory called tmp/. The option --keeptar keeps a tar file that is already made  for a new job for a new model set by --model. The remaining parameters define the input and output directories (in this example they are both on LPC eos).  

### Generating 2D Scan Histograms

The key 2D scans for signal for the RA2 analysis are the signal efficiency, observed significance and upper limit contours and obs limits. The scripts to create 2D smoothed histograms and contours are in DatacardBuilder/plottingStuff. 

For Signal efficiency is the simplest because it is plotted directly from the signal datacards and the efficiency is computed by dividing the cross-section out from the 
integral of the signal over the 174 search bins (gives N_passed/N_total). The script requires a list of files per model and an input list of cross sections (I made formatted .txt files from [SUSY Cross-Sections](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections). An example scan:
    ```
    cd plottingStuff/
    python PlotMassContoursSmoothEfficiency.py --model=T1bbbb --xsec=LatestGluGluNNLO.txt --idir=/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/
    ```
This produces an output file MassScanT1bbbb.root containing a histogram of efficiencies in the 2D mass plane of the T1bbbb model. By default the signal efficiency for models with leptons is adjusted (by degraded the efficiency according to the 1-lepton signal contamination) and the efficiency is computed using the average of the reco MHT and gen MHT binning. The code is setup to run over 4 run eras 2016, 2017, 2018, 2018HEM, but can be modified to just do a single run period.

The significance scan is produced in a similar way using PlotMassContoursSmoothSignif.py where the arguments are the same but the list of files are the resultsYYYY.root (where YYYY are the files made using analysisBuilderCondor.py with the option Significance). 

    ```
    cd plottingStuff/
    ls /eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/Signif/results*T1bbbb*.root > listofFilesT1bbbb.txt
    python PlotMassContoursSmoothSignif.py --model=T1bbbb --xsec=LatestGluGluNNLO.txt --idir=/eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/Signif/
    ```
This produces an output file MassScanT1bbbb.root which contains the observed significance in the 2D mass plane. 

Finally producing the Obs limit in the 2D plane along with the Expected, Observed contours is done in PlotMassContoursSmoothLimit.py

    ```
    cd plottingStuff/
    ls /eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/results*T1bbbb*.root > listofFilesT1bbbb.txt
    python PlotMassContoursSmoothLimit.py --model=T1bbbb --xsec=LatestGluGluNNLO.txt --idir=/eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/
    ```
This will output a file MassScanT1bbbb.root for the Obs and Exp limits in the 2D mass plane as well as the contours for the obs limit, the theory uncertainty, the expected limit (medium, +/- 1sigma, +/- 2sigma)

Just a few notes about the code:
-To create a smooth 2D histogram all of the above code uses TGraph2D where the size of the bins is hard coded in the scripts (this can be adjusted)
-T2qq is a model with 8-squarks but is also used to do the single 1 quark limit, by default in the script the contours drawn are for signal strength of 1.0,
but for the single quark this needs to be adjusted to be 1/8 of the total xsec, so this needs to be changed in the script when running over this model. 
-The significance needs additional smoothing when there are fluctations, this can be done by removing points in the TGraph2D and reinterpolating
-The contours of the limit also sometimes need additional smoothing, which can be done in root using the TGraphSmoothClass and SmoothSuper. 

### Plotting 2D scans
The code used to plot results for 2D SMS mass scans is based on the repository [PlotsSMS](https://github.com/CMS-SUS-XPAG/PlotsSMS) but is modified a bit for the RA2 analysis and the various 2D scans required for the publication and additional material.


## Plots for Publication

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

### Notes for updates

A few parts of the code have hard-coded file paths and variables: 
- scripts/fill_signal_hists.py defines which signal points are stored in the signal histograms, so these can limit what signal is overlayed in plots
- scripts/signal_model.py hard-codes the path to look for the signal input files
- scripts/search_bin.py hard-codes the labels for the RA2 search bins, so these would be changed for any future optimization. 
- scripts/agg_bins.py contains the definition of the aggregate bins based on the summation of the 174 search bins. 
- The bkg estimation scripts: fill_qcd_hists.py,fill_znn_hists.py, and fill_hadtau_hists.py rely on the histogram keys in the input root files to be the same as used in the Run 2 legacy analysis. If these names change, these files need to be updated so that uncertainties are properly summed accounting for correlations.

 
