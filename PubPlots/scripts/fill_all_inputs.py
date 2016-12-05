from fill_znn_hists import *
from fill_lostlep_hists import *
from fill_hadtau_hists import *
from fill_qcd_hists import *
from fill_qcdrs_hists import *
from fill_data_hists import *
from fill_signal_hists import *

def fill_all_inputs(lumi=18077.491):
    fill_data_hists('inputs/data_hists/RA2bin_signal.root', 'RA2bin_data', 'data_hists.root', 174)
##    fill_data_hists('inputs/data_hists/Data_combined_ICHEP_RUNG.root', 'RA2bin_data', 'data_hists.root', 174)
    fill_znn_hists('inputs/bg_hists/ZinvHistos.root', 'znn_hists.root', 174, lumi/36344.959) # CR lumi from single-electron V11
    fill_qcdrs_hists('inputs/bg_hists/QcdPredictionRandS_24.6.root', 'qcdrs_hists.root', 174, lumi/24480.699) # CR lumi from JetHT V10
    fill_lostlep_hists('inputs/bg_hists/LLPrediction_notCombined.root', 'lostlep_hists.root', 174, lumi/36348.547) # CR lumi from MET V11
    fill_hadtau_hists('inputs/bg_hists/ARElog94_36.35fb_HadTauEstimation_data_formatted_V11.root', 'hadtau_hists.root', 174, lumi/36340.749) # CR lumi from single-muon V11
    fill_signal_hists('signal_hists.root', 174)
    fill_qcd_hists('inputs/bg_hists/qcd-bg-combine-input-36.3ifb-dec01-dashes.txt', 'qcd_hists.root', 174, lumi/36348.547) # CR lumi from MET V11

if __name__ == "__main__":
    import sys
    fill_all_inputs(float(sys.argv[1]))
