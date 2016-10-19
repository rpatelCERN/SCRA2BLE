from make_160_bin_plot import make_160_bin_plot
from make_160_bin_tables import make_160_bin_tables
from make_12_asr_plot import make_12_asr_plot
from make_asr_table import make_asr_table
from make_all_1D_projections import make_all_1D_projections
from ROOT import TFile
from bg_est import BGEst
from data_obs import DataObs

def make_all_pas_plots_and_tables(lostlep_file = 'lostlep_hists.root', hadtau_file = 'hadtau_hists.root', znn_file = 'znn_hists.root', qcd_file = 'qcd_hists.root', data_file = 'data_hists.root', signal_file = 'signal_hists.root'):

    # open input files
    f_lostlep = TFile.Open(lostlep_file)
    f_hadtau = TFile.Open(hadtau_file)
    f_qcd = TFile.Open(qcd_file)
    f_znn = TFile.Open(znn_file)
    f_data_obs = TFile.Open(data_file)

    # build obs data and bg estiamtion from input histograms
    data_obs = DataObs(f_data_obs.Get("hCV"))
    qcd = BGEst(f_qcd.Get("hCV"), f_qcd.Get("hStatUp"), f_qcd.Get("hStatDown"), f_qcd.Get("hSystUp"), f_qcd.Get("hSystDown"), 2001)
    znn = BGEst(f_znn.Get("hCV"), f_znn.Get("hStatUp"), f_znn.Get("hStatDown"), f_znn.Get("hSystUp"), f_znn.Get("hSystDown"), 2002)
    lostlep = BGEst(f_lostlep.Get("hCV"), f_lostlep.Get("hStatUp"), f_lostlep.Get("hStatDown"), f_lostlep.Get("hSystUp"), f_lostlep.Get("hSystDown"), 2006)
    hadtau = BGEst(f_hadtau.Get("hCV"), f_hadtau.Get("hStatUp"), f_hadtau.Get("hStatDown"), f_hadtau.Get("hSystUp"), f_hadtau.Get("hSystDown"), 2007)

    make_160_bin_plot('results-plot-prefit-12_9-log', lostlep, hadtau, znn, qcd, data_obs)
    make_160_bin_plot('results-plot-prefit-12_9-log-pull', lostlep, hadtau, znn, qcd, data_obs, True)
    make_160_bin_tables('results-prefit-12_9', lostlep, hadtau, znn, qcd, data_obs)

    ## aggregate search regions
    data_obs_12_asrs = DataObs(f_data_obs.Get("ASR/hCV"))
    qcd_12_asrs = BGEst(f_qcd.Get("ASR/hCV"), f_qcd.Get("ASR/hStatUp"), f_qcd.Get("ASR/hStatDown"), f_qcd.Get("ASR/hSystUp"), f_qcd.Get("ASR/hSystDown"), 2001)
    znn_12_asrs = BGEst(f_znn.Get("ASR/hCV"), f_znn.Get("ASR/hStatUp"), f_znn.Get("ASR/hStatDown"), f_znn.Get("ASR/hSystUp"), f_znn.Get("ASR/hSystDown"), 2002)
    lostlep_12_asrs = BGEst(f_lostlep.Get("ASR/hCV"), f_lostlep.Get("ASR/hStatUp"), f_lostlep.Get("ASR/hStatDown"), f_lostlep.Get("ASR/hSystUp"), f_lostlep.Get("ASR/hSystDown"), 2006)
    hadtau_12_asrs = BGEst(f_hadtau.Get("ASR/hCV"), f_hadtau.Get("ASR/hStatUp"), f_hadtau.Get("ASR/hStatDown"), f_hadtau.Get("ASR/hSystUp"), f_hadtau.Get("ASR/hSystDown"), 2007)

    make_12_asr_plot('results-plot-prefit-12-asrs-log', lostlep_12_asrs, hadtau_12_asrs, znn_12_asrs, qcd_12_asrs, data_obs_12_asrs)
    make_12_asr_plot('results-plot-prefit-12-asrs-log-pull', lostlep_12_asrs, hadtau_12_asrs, znn_12_asrs, qcd_12_asrs, data_obs_12_asrs, True)
    make_asr_table('asr_table', lostlep_12_asrs, hadtau_12_asrs, znn_12_asrs, qcd_12_asrs, data_obs_12_asrs)

    ## 1D projections
    make_all_1D_projections(lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file)

if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    make_all_pas_plots_and_tables(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]) # 
