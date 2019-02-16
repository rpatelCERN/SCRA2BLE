from fill_znn_hists import *
from fill_lostlep_hists import *
from fill_hadtau_hists import *
from fill_qcd_hists import *
from fill_qcdrs_hists import *
from fill_data_hists import *
from fill_signal_hists import *
from fill_postfit import *


def fill_all_inputs(lumi=35862.345):
   #fill_znn_hists('inputs/bg_hists/CrossCheck2016/ZinvHistos_2016.root', 'znn_hists.root', 174) # CR lumi from single-electron V11: 36344.959
   #fill_znn_hists('inputs/bg_hists/ZinvHistosPublished.root', 'znn_hists.root', 174) # CR lumi from single-electron V11: 36344.959
   fill_hadtau_hists('inputs/bg_hists/FullRun2/InputsForLimits_data_formatted_LLPlusHadTau.root', 'lostlept_hists.root', 174,15./137.4) # CR lumi from single-muon V11: 36340.749
   fill_qcdrs_hists('inputs/bg_hists/FullRun2/master-r+s-137.4.root', 'qcdrs_hists.root', 174,15./137.4) # CR lumi from JetHT V11: 36346.489
   #fill_signal_hists('signal_hists.root', 174)
   fill_znn_hists('inputs/bg_hists/FullRun2/ZinvHistos.root', 'znn_hists.root', 174,15./137.4) # CR lumi from single-electron V11: 36344.959
   fill_data_hists('inputs/data_hists/FullRun2/RA2bin_signal.root', 'RA2bin_data2018', 'data_hists.root', 174)
   #fill_postfit('inputs/bg_hists/FullRun2/fitDiagnosticstestCards-allBkgs-T1tttt_2000_100-137.4-mu0.0.root', 'postfit_hists.root',174)
   #fill_qcd_hists('inputs/bg_hists/qcd-bg-combine-input-36.3ifb-dec16-dashes.txt', 'qcd_hists.root', 174) # CR lumi from MET V11: 35862.345
   #fill_qcdrs_hists('inputs/bg_hists/master-r+s-35.9.root', 'qcdrs_hists.root', 174,10./41.5) # CR lumi from JetHT V11: 36346.489
   #fill_znn_hists('inputs/bg_hists/ZinvHistos.root', 'znn_hists.root', 174, 10./41.5) # CR lumi from single-electron V11: 36344.959
   #fill_data_hists('inputs/data_hists/FullRun2/RA2bin_signal.root', 'RA2bin_data2017', 'data_hists.root', 174)
   #fill_data_hists('inputs/data_hists/RA2bin_signal.root', 'RA2bin_data', 'data_hists.root', 174)
   #fill_hadtau_hists('inputs/bg_hists/Run2018Inputs/InputsForLimits_data_formatted_LLPlusHadTau_Run2018.root', 'lostlept_hists.root', 174,15./41.5) # CR lumi from single-muon V11: 36340.749
   #fill_qcdrs_hists('inputs/bg_hists/Run2018Inputs/QcdPredictionRun2018.root', 'qcdrs_hists.root', 174,15./41.5) # CR lumi from JetHT V11: 36346.489
   fill_signal_hists('signal_hists.root', 174)

if __name__ == "__main__":
    import sys
    if len(sys.argv)==1:
        fill_all_inputs()
    else:
        fill_all_inputs(float(sys.argv[1]))
