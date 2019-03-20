from fill_znn_hists import *
from fill_lostlep_hists import *
from fill_hadtau_hists import *
from fill_qcd_hists import *
from fill_qcdrs_hists import *
from fill_data_hists import *
from fill_signal_hists import *
from fill_postfit import *


#def fill_all_inputs(lumi=35862.345):
def fill_all_inputs(year=2016):
   #fill_znn_hists('inputs/bg_hists/ZinvHistosPublished.root', 'znn_hists.root', 174) # CR lumi from single-electron V11: 36344.959
    ####### 15fb for 2018
   #fill_znn_hists('inputs/bg_hists/FullRun2/ZinvHistos.root', 'znn_hists.root', 174,7.8/137.4) # CR lumi from single-electron V11: 36344.959
# CR lumi from single-electron V11: 36344.959
   #fill_hadtau_hists('inputs/bg_hists/Run2018Inputs/NoHEM/InputsForLimits_data_formatted_LLPlusHadTau_PreHEMRecheck.root', 'lostlept_hists.root', 174,7.8/20.92) # CR lumi from single-muon V11: 36340.749
   #fill_hadtau_hists('inputs/bg_hists/FullRun2/InputsForLimits_data_formatted_LLPlusHadTau.root', 'lostlept_hists.root', 174,7.8/137.4) # CR lumi from single-muon V11: 36340.749
   #########2016########################
   if year==2016:
   	#fill_znn_hists('inputs/bg_hists/histograms_35.9fb/ZinvHistos.root', 'znn_hists.root', 174) # CR lumi from single-electron V11: 36344.959
   	#fill_hadtau_hists('inputs/bg_hists/histograms_35.9fb/InputsForLimits_data_formatted_LLPlusHadTauOldBinning.root', 'lostlept_hists.root', 174) # CR lumi from single-muon V11: 36340.749
   	#fill_qcdrs_hists('inputs/bg_hists/histograms_35.9fb/QcdPredictionRandS.root', 'qcdrs_hists.root', 174) # CR lumi from JetHT V11: 36346.489
   	#fill_data_hists('inputs/bg_hists/histograms_35.9fb/RA2bin_signalUnblind.root', 'RA2bin_data', 'data_hists.root', 174)

	fill_qcdrs_hists('inputs/bg_hists/FullRun2/QcdPredictionRun2.root', 'qcdrs_hists.root', 174,61.9/137.4) # CR lumi from JetHT V11: 36346.489
   	fill_znn_hists('inputs/bg_hists/FullRun2/zinvData_2019Feb22_Run2/ZinvHistos.root', 'znn_hists.root', 174,61.9/137.4) # CR lumi from single-electron V11: 36344.959
   	fill_hadtau_hists('inputs/bg_hists/FullRun2/InputsForLimits_data_formatted_LLPlusHadTau_CombinedYears.root', 'lostlept_hists.root', 174,61.9/137.4) # CR lumi from single-muon V11: 36340.749
   	#fill_znn_hists('inputs/bg_hists/CrossCheck2016/zinvData_2019Feb22_2016/ZinvHistos.root', 'znn_hists.root', 174) # CR lumi from single-electron V11: 36344.959
   	#fill_hadtau_hists('inputs/bg_hists/CrossCheck2016/InputsForLimits_data_formatted_LLPlusHadTau_2016.root', 'lostlept_hists.root', 174) # CR lumi from single-muon V11: 36340.749
   	#fill_qcdrs_hists('inputs/bg_hists/CrossCheck2016/QcdPredictionRun2016.root', 'qcdrs_hists.root', 174) # CR lumi from JetHT V11: 36346.489
   	fill_data_hists('inputs/data_hists/data_fixhtratio/RA2bin_signal.root', 'RA2bin_data2016', 'data_hists.root', 174)
   	fill_postfit('inputs/bg_hists/fitDiagnosticstestCards-Moriond-T1tttt_2000_100-61.9-mu0.0.root', 'postfit_hists.root',174)
   if year==2017:
	print(year)
   	#######10fb for 2017
   	fill_znn_hists('inputs/bg_hists/Run2017Inputs/zinvData_2019Feb22_2017/ZinvHistos.root', 'znn_hists.root', 174,10./41.5) # CR lumi from single-electron V11: 36344.959
   	fill_hadtau_hists('inputs/bg_hists/Run2017Inputs/InputsForLimits_data_formatted_LLPlusHadTau_Run2017.root', 'lostlept_hists.root', 174,10./41.5) # CR lumi from single-muon V11: 36340.749
   	fill_qcdrs_hists('inputs/bg_hists/Run2017Inputs/QcdPredictionRun2017.root', 'qcdrs_hists.root', 174,10./41.5) # CR lumi from JetHT V11: 36346.489
   	fill_data_hists('inputs/data_hists/data_fixhtratio/RA2bin_signal.root', 'RA2bin_data2017', 'data_hists.root', 174)
   	#fill_postfit('inputs/bg_hists/fitDiagnosticstestCards-Moriond-T1tttt_2000_100-10.0-mu0.0.root', 'postfit_hists.root',174)

   if year==2018:
	#fill_qcdrs_hists('inputs/bg_hists/Run2018Inputs/QcdPredictionRun2018PreHem.root', 'qcdrs_hists.root', 174,7.8/20.92) # CR lumi from JetHT V11: 36346.489
   	#fill_znn_hists('inputs/bg_hists/Run2018Inputs/zinvData_2019Feb22_2018AB/ZinvHistos.root', 'znn_hists.root', 174,7.8/20.92) # CR lumi from single-electron V11: 36344.959
   	#fill_hadtau_hists('inputs/bg_hists/Run2018Inputs/NoHEM/InputsForLimits_data_formatted_LLPlusHadTau_PreHEMRecheck.root', 'lostlept_hists.root', 174,7.8/20.92) # CR lumi from single-muon V11: 36340.749
   	#fill_data_hists('inputs/data_hists/data_fixhtratio/RA2bin_signal.root', 'RA2bin_data2018', 'data_hists.root', 174)
   	fill_znn_hists('inputs/bg_hists/Run2018Inputs/zinvData_2019Feb22_2018CD/ZinvHistos.root', 'znn_hists.root', 174,8.2/38.83) 
   	fill_hadtau_hists('inputs/bg_hists/Run2018Inputs/HEM/InputsForLimits_data_formatted_LLPlusHadTau_PostHEMRecheck.root', 'lostlept_hists.root', 174,8.2/38.83) # CR lumi from single-muon V11: 36340.749
   	fill_qcdrs_hists('inputs/bg_hists/Run2018Inputs/QcdPredictionRun2018PostHem.root', 'qcdrs_hists.root', 174,8.2/38.83) # CR lumi from JetHT V11: 36346.489
   	#fill_data_hists('inputs/data_hists/data_fixhtratio/RA2bin_signal.root', 'RA2bin_data2018HEM', 'data_hists.root', 174)
   	fill_data_hists('inputs/data_hists/data_althemveto/RA2bin_signal.root', 'RA2bin_data2018HEM_ra2bin2018HEM-alt2', 'data_hists.root', 174)
	
   #fill_znn_hists('inputs/bg_hists/Run2018Inputs/HEM/ZinvHistos.root', 'znn_hists.root', 174,8.2/38.83) 
   #fill_znn_hists('inputs/bg_hists/CrossCheck2016/zinvData_2019Feb17_Run2016/ZinvHistos.root', 'znn_hists.root', 174) # CR lumi from single-electron V11: 36344.959
   	'''
   ##############2018A######################
   ##############2018D######################
  # fill_data_hists('inputs/data_hists/RA2bin_signal.root', 'RA2bin_data', 'data_hists.root', 174)
   #fill_hadtau_hists('inputs/bg_hists/Run2018Inputs/InputsForLimits_data_formatted_LLPlusHadTau_Run2018.root', 'lostlept_hists.root', 174,15./41.5) # CR lumi from single-muon V11: 36340.749
   #fill_znn_hists('inputs/bg_hists/Run2018Inputs/ZinvHistosFullRun2.root', 'znn_hists.root', 174,15./137.4) # CR lumi from single-electron V11: 36344.959
   #fill_qcdrs_hists('inputs/bg_hists/Run2018Inputs/QcdPredictionRun2018.root', 'qcdrs_hists.root', 174,15./41.5) # CR lumi from JetHT V11: 36346.489
   #fill_data_hists('inputs/data_hists/RA2bin_signalEventList.root', 'RA2bin_data2017_ra2bin2017', 'data_hists.root')
   #fill_data_hists('inputs/data_hists/FullRun2/HEMVETO/RA2bin_signalNoHEM.root', 'RA2bin_data2018HEM', 'data_hists.root')
   #fill_data_hists('inputs/data_hists/FullRun2/HEMVETOFix/RA2bin_signal.root', 'RA2bin_data2018HEM', 'data_hists.root')
   #fill_data_hists('inputs/data_hists/FullRun2/HEMVETOFix/RA2bin_signal.root', 'RA2bin_data2018HEM', 'data_hists.root')
   #fill_signal_hists('signal_hists.root', 174)
   #fill_qcd_hists('inputs/bg_hists/qcd-bg-combine-input-36.3ifb-dec16-dashes.txt', 'qcd_hists.root', 174) # CR lumi from MET V11: 35862.345
   #fill_qcdrs_hists('inputs/bg_hists/master-r+s-35.9.root', 'qcdrs_hists.root', 174,10./41.5) # CR lumi from JetHT V11: 36346.489
   #fill_znn_hists('inputs/bg_hists/ZinvHistos.root', 'znn_hists.root', 174, 10./41.5) # CR lumi from single-electron V11: 36344.959
   fill_signal_hists('signal_hists.root', 174)
   '''
if __name__ == "__main__":
    import sys
    if len(sys.argv)==1:
        fill_all_inputs()
    else:
        fill_all_inputs(int(sys.argv[1]))
