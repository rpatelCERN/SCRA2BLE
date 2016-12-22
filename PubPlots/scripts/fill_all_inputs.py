from fill_znn_hists import *
from fill_lostlep_hists import *
from fill_hadtau_hists import *
from fill_qcd_hists import *
from fill_qcdrs_hists import *
from fill_data_hists import *
from fill_signal_hists import *


def fill_all_inputs(lumi=36348.547):
   fill_data_hists('inputs/data_hists/Data_174Bins_SR_Moriond2017_36.3.root', 'RA2bin_data', 'data_hists.root', 174)
   fill_znn_hists('inputs/bg_hists/ZinvHistos.root', 'znn_hists.root', 174) # CR lumi from single-electron V11: 36344.959
   fill_qcdrs_hists('inputs/bg_hists/QcdPredictionRandS_36.3.root', 'qcdrs_hists.root', 174) # CR lumi from JetHT V11: 36346.489
   fill_lostlep_hists('inputs/bg_hists/LLPrediction.root', 'lostlep_hists.root', 174) # CR lumi from MET V11: 36348.547
   fill_hadtau_hists('inputs/bg_hists/ARElog98_36.35ifb_HadTauEstimation_data_formatted_V11.root', 'hadtau_hists.root', 174) # CR lumi from single-muon V11: 36340.749
   fill_signal_hists('signal_hists.root', 174)
   fill_qcd_hists('inputs/bg_hists/qcd-bg-combine-input-36.3ifb-dec16-dashes.txt', 'qcd_hists.root', 174) # CR lumi from MET V11: 36348.547

if __name__ == "__main__":
    import sys
    fill_all_inputs(float(sys.argv[1]))
