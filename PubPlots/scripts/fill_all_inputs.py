from fill_znn_hists import *
from fill_lostlep_hists import *
from fill_hadtau_hists import *
from fill_qcd_hists import *
from fill_qcdrs_hists import *
from fill_data_hists import *
from fill_signal_hists import *
from fill_postfit import *


#def fill_all_inputs(lumi=35862.345):
def fill_all_inputs(year=""):
	if year=="":#Merged years do not have run dependent behavior
		fill_qcdrs_hists('../DatacardBuilder/inputHistograms/histograms_137.4fb/QcdPredictionRandS.root', 'qcdrs_hists.root', 174)
		fill_znn_hists('../DatacardBuilder/inputHistograms/histograms_137.4fb/ZinvHistos.root', 'znn_hists.root', 174) 
		fill_hadtau_hists('../DatacardBuilder/inputHistograms/histograms_137.4fb/InputsForLimits_data_formatted_LLPlusHadTau.root', 'lostlept_hists.root', 174) 
		fill_data_hists('../DatacardBuilder/inputHistograms/histograms_137.4fb/RA2bin_signalUnblindMerged.root', 'RA2bin_data_Unblind', 'data_hists.root', 174)
#########Run dependent plots:
	if year=="2016":
		#Bkg estimates derived only from the 2016 data 35.9/fb
		fill_znn_hists('inputs/bg_hists/Run2016Inputs/ZinvHistos.root', 'znn_hists.root', 174) 
        	fill_hadtau_hists('inputs/bg_hists/Run2016Inputs/InputsForLimits_data_formatted_LLPlusHadTau_2016.root', 'lostlept_hists.root', 174)
        	fill_qcdrs_hists('inputs/bg_hists/Run2016Inputs/QcdPredictionRun2016.root', 'qcdrs_hists.root', 174) 
	        fill_data_hists('inputs/data_hists/FullRun2/RA2bin_signalUnblind.root', 'RA2bin_data2016', 'data_hists.root', 174)		
	if year=="2017":
		#Bkg estimates derived only from the 2017 data 41.0/fb
		fill_znn_hists('inputs/bg_hists/Run2017Inputs/ZinvHistos.root', 'znn_hists.root', 174) 
        	fill_hadtau_hists('inputs/bg_hists/Run2017Inputs/InputsForLimits_data_formatted_LLPlusHadTau_Run2017.root', 'lostlept_hists.root', 174)
        	fill_qcdrs_hists('inputs/bg_hists/Run2017Inputs/QcdPredictionRun2017.root', 'qcdrs_hists.root', 174) 
	        fill_data_hists('inputs/data_hists/FullRun2/RA2bin_signalUnblind.root', 'RA2bin_data2017', 'data_hists.root', 174)		
	if year=="2018":
		#Bkg estimates derived only from the 2017 data 41.0/fb
		fill_znn_hists('inputs/bg_hists/Run2018Inputs/NoHEM/ZinvHistos.root', 'znn_hists.root', 174) 
        	fill_hadtau_hists('inputs/bg_hists/Run2018Inputs/NoHEM/InputsForLimits_data_formatted_LLPlusHadTau_PreHEMRecheck.root', 'lostlept_hists.root', 174)
        	fill_qcdrs_hists('inputs/bg_hists/Run2018Inputs/NoHEM/QcdPredictionRun2018PreHem.root', 'qcdrs_hists.root', 174) 
	        fill_data_hists('inputs/data_hists/FullRun2/RA2bin_signalUnblind.root', 'RA2bin_data2018', 'data_hists.root', 174)		
	if year=="2018HEM":
		#Bkg estimates derived only from the 2017 data 41.0/fb
		fill_znn_hists('inputs/bg_hists/Run2018Inputs/HEM/ZinvHistos.root', 'znn_hists.root', 174) 
        	fill_hadtau_hists('inputs/bg_hists/Run2018Inputs/HEM/InputsForLimits_data_formatted_LLPlusHadTau_PostHEMRecheck.root', 'lostlept_hists.root', 174)
        	fill_qcdrs_hists('inputs/bg_hists/Run2018Inputs/HEM/QcdPredictionRun2018PostHem.root', 'qcdrs_hists.root', 174) 
	        fill_data_hists('inputs/data_hists/FullRun2/RA2bin_signalUnblind.root', 'RA2bin_data2018HEM', 'data_hists.root', 174)		
	#These are only derived for the full data
	fill_signal_hists('signal_hists.root', 174)
	fill_postfit('inputs/bg_hists/FullRun2/fitDiagnosticstestCards-Moriond-T1tttt_1500_100-137.4-mu0.0.root', 'postfit_hists.root',174)

if __name__ == "__main__":
    import sys
    if len(sys.argv)==1:
        fill_all_inputs()
    else:
        fill_all_inputs(sys.argv[1])
