from fill_znn_hists import *
from fill_lostlep_hists import *
from fill_hadtau_hists import *
from fill_qcd_hists import *
from fill_data_hists import *
from fill_signal_hists import *

fill_data_hists('inputs/data_hists/Data_174Bins_SR_DryRun_12.9.root', 'data_hists.root', 174)
fill_znn_hists('inputs/bg_hists/ZinvHistos.root', 'znn_hists.root', 174)
fill_lostlep_hists('inputs/bg_hists/LLPrediction.root', 'lostlep_hists.root', 174)
fill_hadtau_hists('inputs/bg_hists/HadTauEstimation_data_formatted.root', 'hadtau_hists.root', 174)
fill_qcd_hists('inputs/bg_hists/qcd-bg-combine-input-24.5ifb-nov4-dashes.txt', 'qcd_hists.root', 174)
fill_signal_hists('signal_hists.root', 174)
