import make_160_bin_plot
import make_160_bin_tables
from ROOT import TFile
from bg_est import BGEst
from data_obs import DataObs

def make_all_summary_plots(lostlep_file = 'lostlep_hists.root', hadtau_file = 'hadtau_hists.root', znn_file = 'znn_hists.root', qcd_file = 'qcd_hists.root', data_file = 'inputs/data_hists/Data_160Bins_SR_Approval_12.9.root'):

    # open input files
    f_lostlep = TFile.Open(lostlep_file)
    f_hadtau = TFile.Open(hadtau_file)
    f_qcd = TFile.Open(qcd_file)
    f_znn = TFile.Open(znn_file)
    f_data_obs = TFile.Open(data_file)

    # build obs data and bg estiamtion from input histograms
    data_obs = DataObs(f_data_obs.Get("data"))
    qcd = BGEst(f_qcd.Get("hCV"), f_qcd.Get("hStatUp"), f_qcd.Get("hStatDown"), f_qcd.Get("hSystUp"), f_qcd.Get("hSystDown"), 2001)
    znn = BGEst(f_znn.Get("hCV"), f_znn.Get("hStatUp"), f_znn.Get("hStatDown"), f_znn.Get("hSystUp"), f_znn.Get("hSystDown"), 2002)
    lostlep = BGEst(f_lostlep.Get("hCV"), f_lostlep.Get("hStatUp"), f_lostlep.Get("hStatDown"), f_lostlep.Get("hSystUp"), f_lostlep.Get("hSystDown"), 2006)
    hadtau = BGEst(f_hadtau.Get("hCV"), f_hadtau.Get("hStatUp"), f_hadtau.Get("hStatDown"), f_hadtau.Get("hSystUp"), f_hadtau.Get("hSystDown"), 2007)

    
    make_160_bin_plot.make_160_bin_plot('results-plot-prefit-12_9-log', lostlep, hadtau, znn, qcd, data_obs)
    make_160_bin_tables.make_160_bin_tables('results-prefit-12_9', lostlep, hadtau, znn, qcd, data_obs)

if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    make_all_summary_plots(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]) # 
