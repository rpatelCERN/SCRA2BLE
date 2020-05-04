# SCRA2BLE

The RA2 SCRA2BLE integration code is designed to perform the necessary steps to produce the results, diagnostics,and statistical 
interpretations by combining the latest version of the background estimates into a figure or into a likelihood model. The two folders in this repository split the code into these two main functions: plotting integration results  (PubPlots) and performing likelihood fitting or diagonostics (DatacardBuilder). 

The current version of the code is based on the legacy 13 TeV [RA2 analysis](https://arxiv.org/abs/1908.04722), which 
used 174 search bins with seperate background inputs for each Run era based on the data taking periods in 2016, 2017, 2018 
(further split by HEM affected runs). The analysis used the RA2 production from the [Treemaker](https://github.com/TreeMaker/TreeMaker/tree/Run2_2017) and the signal histograms from the V17 signal samples. 

# # Setup 

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

```
git clone -b Run2LegacyPub  https://github.com/rpatelCERN/SCRA2BLE.git
```

# # Plots for Publication

The files necessary to produce plots for a PAS, publication, supplementary material, or for the technical twiki page are produced from the code in PubPlots.

```
cd PubPlots
python scripts/fill_all_inputs.py YEAR
```

The above function will create formatted histograms for the bkg estimate, data, post-fit backgrounds, and selected signal points. The bkg and data are filled according to Run Eras (2016,2017, 2018, 2018HEM) 
