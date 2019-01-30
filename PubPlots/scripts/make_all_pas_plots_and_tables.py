from make_174_bin_plot import make_174_bin_plot
#from make_174_bin_postfitplot import make_174_bin_postfitplot
from make_1d_pull_dist import make_1d_pull_dist
from make_174_bin_tables import make_174_bin_tables
from make_12_asr_plot import make_12_asr_plot
from make_asr_table import make_asr_table
from make_all_1D_projections import make_all_1D_projections
from ROOT import gROOT
from ROOT import TFile
from bg_est import BGEst
from data_obs import DataObs
gROOT.SetBatch(True)
def make_all_pas_plots_and_tables(lostlept_file = 'lostlept_hists.root', znn_file = 'znn_hists.root', qcd_file = 'qcdrs_hists.root', data_file = 'data_hists.root', signal_file = 'signal_hists.root',postfitFile="postfit_hists.root"):

    # open input files
    f_lostlept = TFile.Open(lostlept_file)
    #f_hadtau = TFile.Open(hadtau_file)
    f_qcd = TFile.Open(qcd_file)
    f_znn = TFile.Open(znn_file)
    f_data_obs = TFile.Open(data_file)
    f_postfit=TFile(postfitFile)
    # build obs data and bg estiamtion from input histograms
    data_obs = DataObs(f_data_obs.Get("hCV"))
    #postfitZ =DataObs(f_postfit.Get("Zinv"));
    #postfitQCD =DataObs(f_postfit.Get("QCD"));
    #postfitLL =DataObs(f_postfit.Get("LL"));
    qcd = BGEst(f_qcd.Get("hCV"), f_qcd.Get("hStatUp"), f_qcd.Get("hStatDown"), f_qcd.Get("hSystUp"), f_qcd.Get("hSystDown"), 2001)
    znn = BGEst(f_znn.Get("hCV"), f_znn.Get("hStatUp"), f_znn.Get("hStatDown"), f_znn.Get("hSystUp"), f_znn.Get("hSystDown"), 2002)
    lostlept = BGEst(f_lostlept.Get("hCV"), f_lostlept.Get("hStatUp"), f_lostlept.Get("hStatDown"), f_lostlept.Get("hSystUp"), f_lostlept.Get("hSystDown"), 2006)

    qcdPost = BGEst(f_postfit.Get("QCDCV"), f_postfit.Get("QCDStat"), f_postfit.Get("QCDStat"), f_postfit.Get("QCDSys"), f_postfit.Get("QCDSys"), 2001)
    znnPost = BGEst(f_postfit.Get("ZinvCV"), f_postfit.Get("ZinvStat"), f_postfit.Get("ZinvStat"), f_postfit.Get("ZinvSys"), f_postfit.Get("ZinvSys"), 2002)
    lostleptPost = BGEst(f_postfit.Get("LLCV"), f_postfit.Get("LLStat"), f_postfit.Get("LLStat"), f_postfit.Get("LLSys"), f_postfit.Get("LLSys"), 2006)
     
    make_174_bin_plot('results-plot-postfit-40_5_pre_app-log',  lostleptPost, znnPost, qcdPost, data_obs)
    make_174_bin_plot('results-plot-prefit-35_9_pre_app-log',  lostlept, znn, qcd, data_obs)
    make_174_bin_plot('results-plot-prefit-35_9_pre_app-log-pull',  lostlept, znn, qcd, data_obs, True)
    make_1d_pull_dist('results-prefit-pulls-1D-35_9-pre_app',  lostlept, znn, qcd, data_obs)
    make_174_bin_tables('results-prefit-tables-35_9_pre_app',  lostlept, znn, qcd, data_obs)
    make_174_bin_tables('results-postfit-tables-35_9_pre_app',  lostleptPost, znnPost, qcdPost, data_obs)

    ## aggregate search regions
    data_obs_12_asrs = DataObs(f_data_obs.Get("ASR/hCV"))
    qcd_12_asrs = BGEst(f_qcd.Get("ASR/hCV"), f_qcd.Get("ASR/hStatUp"), f_qcd.Get("ASR/hStatDown"), f_qcd.Get("ASR/hSystUp"), f_qcd.Get("ASR/hSystDown"), 2001)
    znn_12_asrs = BGEst(f_znn.Get("ASR/hCV"), f_znn.Get("ASR/hStatUp"), f_znn.Get("ASR/hStatDown"), f_znn.Get("ASR/hSystUp"), f_znn.Get("ASR/hSystDown"), 2002)
    lostlept_12_asrs = BGEst(f_lostlept.Get("ASR/hCV"), f_lostlept.Get("ASR/hStatUp"), f_lostlept.Get("ASR/hStatDown"), f_lostlept.Get("ASR/hSystUp"), f_lostlept.Get("ASR/hSystDown"), 2006)

    make_12_asr_plot('results-plot-prefit-12-asrs-35_9-log',  lostlept_12_asrs, znn_12_asrs, qcd_12_asrs, data_obs_12_asrs)
    make_12_asr_plot('results-plot-prefit-12-asrs-35_9-log-pull',  lostlept_12_asrs, znn_12_asrs, qcd_12_asrs, data_obs_12_asrs, True)
    make_asr_table('asr_table',  lostlept_12_asrs, znn_12_asrs, qcd_12_asrs, data_obs_12_asrs)

    ## 1D projections
    make_all_1D_projections(lostlept_file, znn_file, qcd_file, data_file, signal_file)

if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    if len(sys.argv) == 1: # no command line inputs -- just use defaults
       make_all_pas_plots_and_tables()
    else:
        make_all_pas_plots_and_tables(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]) #
