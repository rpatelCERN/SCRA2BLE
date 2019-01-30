from fill_znn_hists import *
from fill_lostlep_hists import *
from fill_hadtau_hists import *
from fill_qcd_hists import *
from fill_qcdrs_hists import *
from fill_data_hists import *
from fill_signal_hists import *
from fill_postfit import *


def fill_all_inputs(lumi=35862.345):
   fill_data_hists('inputs/data_hists/yields.root', 'data', 'data_hists.root', 174)
   fill_znn_hists('inputs/bg_hists/ZinvHistos.root', 'znn_hists.root', 174) # CR lumi from single-electron V11: 36344.959
   fill_qcdrs_hists('inputs/bg_hists/master-r+s-35.9.root', 'qcdrs_hists.root', 174) # CR lumi from JetHT V11: 36346.489
   fill_hadtau_hists('inputs/bg_hists/InputsForLimits_data_formatted_LLPlusHadTau.root', 'lostlept_hists.root', 174) # CR lumi from single-muon V11: 36340.749
   fill_signal_hists('signal_hists.root', 174)
   fill_postfit('inputs/bg_hists/fitDiagnosticstestCards-allBkgs-T1tttt_2000_200-41.5-mu0.0.root', 'postfit_hists.root',174)
   #fill_qcd_hists('inputs/bg_hists/qcd-bg-combine-input-36.3ifb-dec16-dashes.txt', 'qcd_hists.root', 174) # CR lumi from MET V11: 35862.345

if __name__ == "__main__":
    import sys
    if len(sys.argv)==1:
        fill_all_inputs()
    else:
        fill_all_inputs(float(sys.argv[1]))
