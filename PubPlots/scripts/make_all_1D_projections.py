from make_1D_projection import make_1D_projection
from ROOT import TFile, gROOT
from bg_est import BGEst
from data_obs import DataObs




def make_all_1D_projections(lostlep_file = 'lostlep_hists.root', hadtau_file = 'hadtau_hists.root', znn_file = 'znn_hists.root', qcd_file = 'qcd_hists.root', data_file = 'data_hists.root'):


    ## T1tttt plot: 2+ b-jets, MHT > 500, HT > 500
    make_12_asr_plot.make_12_asr_plot('results-plot-prefit-12-asrs-log', 'NJ_NB2to3_HTMHT5to10', lostlep_file, hadtau_file, znn_file, qcd_file, data_obs_file)
    make_12_asr_plot.make_12_asr_plot('results-plot-prefit-12-asrs-log-pull', lostlep_file, hadtau_file, znn_file, qcd_file, data_obs_file, True)

if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    make_all_summary_plots(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]) # 
