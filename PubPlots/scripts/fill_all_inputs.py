import fill_znn_hists
import fill_lostlep_hists
import fill_hadtau_hists
import fill_qcd_hists
import fill_data_hists
import fill_signal_hists

fill_data_hists.fill_data_hists('inputs/data_hists/Data_160Bins_SR_Approval_12.9.root', 'data_hists.root', 160)
fill_znn_hists.fill_znn_hists('inputs/bg_hists/ZinvHistos.root', 'znn_hists.root', 160)
fill_lostlep_hists.fill_lostlep_hists('inputs/bg_hists/LLPrediction_Jul26_newSF.root', 'lostlep_hists.root', 160)
fill_hadtau_hists.fill_hadtau_hists('inputs/bg_hists/ARElog60_12.9ifb_HadTauEstimation_data_formatted_New.root', 'hadtau_hists.root', 160)
fill_qcd_hists.fill_qcd_hists('inputs/bg_hists/qcd-bg-combine-input-12.9ifb-july28-nodashes.txt', 'qcd_hists.root', 160)
fill_signal_hists.fill_signal_hists('signal_hists.root', 160)
