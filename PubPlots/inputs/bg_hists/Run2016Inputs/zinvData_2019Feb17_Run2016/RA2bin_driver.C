{
  gROOT->Reset();
  gROOT->ProcessLine(".L ../src/RA2bin_inputs_Zinv.C+");

  std::vector< std::pair<TString, float> > gJetsInputs = {
    std::make_pair("../datFiles/gJets_2016v16_DR2016wt", 35.9)
    // std::make_pair("../datFiles/gJets_2017v16_ZptWt_DR2017wt", 41.5)
    // std::make_pair("../datFiles/gJets_2016v16_ZptWt_DRwt", 35.9)
// ,
//     std::make_pair("../datFiles/gJets_2017v16_ZptWt_DRwt", 41.5),
//     std::make_pair("../datFiles/gJets_2018v16_ZptWt_DRwt", 21.1),
//     std::make_pair("../datFiles/gJets_2018HEMv16_ZptWt_DRwt", 38.3)
  };
  // RA2bin_inputs_Zinv(LDP, gJetsInputs, "../datFiles/DR_Run2", "../datFiles/DY_Run2", "../plots/histograms/ZinvMCttzMC174bin_2016v16.root", 136.8/35.9, true);
  // RA2bin_inputs_Zinv(HDP, gJetsInputs, "../datFiles/DR_Run2", "../datFiles/DY_Run2", "../plots/histograms/ZinvMCttzMC174bin_2016v16.root", 136.8/35.9, true);
  RA2bin_inputs_Zinv(Signal, gJetsInputs, "../datFiles/DR_2016v16_DR2016wt_noPU", "../datFiles/DY_2016v16_noPU",
  		     "../plots/histograms/ZinvMCttzMC174bin_2016v16.root", 35.9/35.9, true);
  // RA2bin_inputs_Zinv(Signal, gJetsInputs, "../datFiles/DR_2017v16_ZptWt_DR2017wt", "../datFiles/DY_2017v16_ZptWt",
  // 		     "../plots/histograms/ZinvMCttzMC174bin_2017v16_ZptWt.root", 41.5/41.5, true);
  // RA2bin_inputs_Zinv(Signal, gJetsInputs, "../datFiles/DR_Run2v16_ZptWt_DRwt", "../datFiles/DY_Run2v16_ZptWt_noJ",
		     // "../plots/histograms/ZinvMCttzMC174bin_Run2v16_ZptWt.root", 136.8/136.8, true);

  
}
