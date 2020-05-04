from make_174_bin_plot import make_174_bin_plot
from make_174_bin_Comp import make_174_bin_Comp
from make_174_bin_CompUnc import make_174_bin_CompUnc
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
from make_1D_postfitprojection import make_1D_postfitprojection
gROOT.SetBatch(True)
def make_all_pas_plots_and_tables(lumiprefix="137Paper",lostlept_file = 'lostlept_hists.root', znn_file = 'znn_hists.root', qcd_file = 'qcdrs_hists.root', data_file = 'data_hists.root', signal_file = 'signal_hists.root',postfitFile="postfit_hists.root"):

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
     
    #make_174_bin_plot('results-plot-postfit-%s_pre_app-pull' %lumiprefix,  lostleptPost, znnPost, qcdPost, data_obs,True,137, 2018)
    #make_174_bin_plot('results-plot-postfit-%s_pre_app-log' %lumiprefix,  lostleptPost, znnPost, qcdPost, data_obs,False,137, 2018)
    #make_174_bin_plot('results-plot-prefit%sfb%d_pre-app-pull' %(lumiprefix,137),  lostlept, znn, qcd, data_obs, True,137,2018)
    #make_174_bin_plot('results-plot-postfit-%s_pre_app-log' %lumiprefix,  lostleptPost, znnPost, qcdPost, data_obs,False,137, 2018)
    #make_1d_pull_dist('results-prefit-pulls-1D-%s-pre_app' %lumiprefix,  lostlept, znn, qcd, data_obs,137)
    #make_1d_pull_dist('results-postfit-pulls-1D-%s-pre_app' %lumiprefix,  lostleptPost, znnPost, qcdPost, data_obs,137)
    make_174_bin_tables('results-prefit-tables-%s_pre_app'%lumiprefix,  lostlept, znn, qcd, data_obs)
    #make_174_bin_tables('results-postfit-tables-%s_app'%lumiprefix,  lostleptPost, znnPost, qcdPost, data_obs)
    #make_174_bin_tables('results-postfit-tables-38.2_pre_app',  lostleptPost, znnPost, qcdPost, data_obs)

    make_174_bin_plot('results-plot-prefit-%s_pre_app-log' %lumiprefix,  lostlept, znn, qcd, data_obs,False,137,2018)
    
    ## aggregate search regions
    #data_obs_12_asrs = DataObs(f_data_obs.Get("ASR/hCV"))
    #qcd_12_asrs = BGEst(f_qcd.Get("ASR/hCV"), f_qcd.Get("ASR/hStatUp"), f_qcd.Get("ASR/hStatDown"), f_qcd.Get("ASR/hSystUp"), f_qcd.Get("ASR/hSystDown"), 2001)
    #znn_12_asrs = BGEst(f_znn.Get("ASR/hCV"), f_znn.Get("ASR/hStatUp"), f_znn.Get("ASR/hStatDown"), f_znn.Get("ASR/hSystUp"), f_znn.Get("ASR/hSystDown"), 2002)
    #lostlept_12_asrs = BGEst(f_lostlept.Get("ASR/hCV"), f_lostlept.Get("ASR/hStatUp"), f_lostlept.Get("ASR/hStatDown"), f_lostlept.Get("ASR/hSystUp"), f_lostlept.Get("ASR/hSystDown"), 2006)

    #make_12_asr_plot('results-plot-prefit-12-asrs-%s-log' %lumiprefix,  lostlept_12_asrs, znn_12_asrs, qcd_12_asrs, data_obs_12_asrs,False, 137)
    #make_12_asr_plot('results-plot-prefit-12-asrs-%s-log-pull'%lumiprefix,  lostlept_12_asrs, znn_12_asrs, qcd_12_asrs, data_obs_12_asrs, True,35.9)
    #make_asr_table('asr_table%s' %lumiprefix,  lostlept_12_asrs, znn_12_asrs, qcd_12_asrs, data_obs_12_asrs)
    #make_1D_postfitprojection('njets-projectionpostfit', 'NJ', "postfit_hists.root"  , data_file,signal_file,\
    #                   "T1tttt_2000_100", "T1tttt_1200_800", "H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, False, True)
    #make_1D_postfitprojection('njets-projectionpostfit-pull', 'NJ', "postfit_hists.root"  , data_file,signal_file,\
    #                   "T1tttt_2000_100", "T1tttt_1200_800", "H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, True, True)
    ## BTags projection
    #make_1D_postfitprojection('nbjets-projectionpostfit', 'NB',  "postfit_hists.root"  , data_file,signal_file, \
    #                   "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 2, H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, False, True)
    #make_1D_postfitprojection('nbjets-projectionpostfit-pull', 'NB',  "postfit_hists.root", data_file, signal_file, \
    #                   "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 2, H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, True, True)
    ## MHT projection
    #make_1D_postfitprojection('mht-projectionpostfit', 'MHT',  "postfit_hists.root", data_file, signal_file, \
    #                   "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 2, H_{T} > 300 GeV", True, False, True)
    #make_1D_postfitprojection('mht-projectionpostfit-pull', 'MHT', "postfit_hists.root", data_file, signal_file, \
    #                   "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 2, H_{T} > 300 GeV", True, True, True)
    ## 1D projections
    #make_all_1D_projections(lostlept_file, znn_file, qcd_file, data_file, signal_file)
    #make_174_bin_Comp('CompPlotYearsZ2017',"inputs/bg_hists/CrossCheck2016/zinvData_2019Feb22_2016/ZinvHistos.root"  ,"inputs/bg_hists/FullRun2/zinvData_2019Feb22_Run2/ZinvHistos.root","Z( #nu #nu)  ", "ZinvBGpred",41.5/137.4)
    #make_174_bin_Comp('CompPlotYearsLL2017',"inputs/bg_hists/CrossCheck2016/InputsForLimits_data_formatted_LLPlusHadTau_2016.root"  ,"inputs/bg_hists/FullRun2/InputsForLimits_data_formatted_LLPlusHadTau_CombinedYears.root","Lost Lept  ", "totalPred_LLPlusHadTau",41.5/137.4)
    #make_174_bin_Comp('CompPlotYearsQCD2017',"inputs/bg_hists/CrossCheck2016/QcdPredictionRun2016.root"  ,"inputs/bg_hists/FullRun2/QcdPredictionRun2.root","QCD R+S  ", "PredictionCV",41.5/137.4)
    #make_174_bin_Comp('CompPlotYearsZ2017',"inputs/bg_hists/Run2017Inputs/zinvData_2019Feb22_2017/ZinvHistos.root"  ,"inputs/bg_hists/FullRun2/zinvData_2019Feb22_Run2/ZinvHistos.root","Z( #nu #nu)  ", "ZinvBGpred",41.5/137.4)
    #make_174_bin_Comp('CompPlotYearsLL2017',"inputs/bg_hists/Run2017Inputs/InputsForLimits_data_formatted_LLPlusHadTau_Run2017.root"  ,"inputs/bg_hists/FullRun2/InputsForLimits_data_formatted_LLPlusHadTau_CombinedYears.root","Lost Lept  ", "totalPred_LLPlusHadTau",41.5/137.4)
    #make_174_bin_Comp('CompPlotYearsQCD2017',"inputs/bg_hists/Run2017Inputs/QcdPredictionRun2017.root"  ,"inputs/bg_hists/FullRun2/QcdPredictionRun2.root","QCD R+S  ", "PredictionCV",41.5/137.4)
    #make_174_bin_Comp('CompPlotYearsZ2018',"inputs/bg_hists/Run2018Inputs/zinvData_2019Feb22_2018AB/ZinvHistos.root"  ,"inputs/bg_hists/Run2018Inputs/zinvData_2019Feb22_2018CD/ZinvHistos.root","Z( #nu #nu)  ", "ZinvBGpred",27.8.905/38196.951)
    #make_174_bin_Comp('CompPlotYearsLL2018',"inputs/bg_hists/Run2018Inputs/NoHEM/InputsForLimits_data_formatted_LLPlusHadTau_PreHEMRecheck.root"  ,"inputs/bg_hists/Run2018Inputs/HEM/InputsForLimits_data_formatted_LLPlusHadTau_PostHEMRecheck.root","Lost Lept  ", "totalPred_LLPlusHadTau",27.8.905/38196.951)
    #make_174_bin_Comp('CompPlotYearsQCD2018',"inputs/bg_hists/Run2018Inputs/QcdPredictionRun2018PreHem.root"  ,"inputs/bg_hists/Run2018Inputs/QcdPredictionRun2018PostHem.root","QCD R+S  ", "PredictionCV",27.8.905/38196.951)
    #make_174_bin_plot('results-plot-prefit7fb2018_FullRun2Inputs',  lostlept, znn, qcd, data_obs, True)
    #make_174_bin_plot('results-plot-prefit8p2fb2018_Inputs',  lostlept, znn, qcd, data_obs, True)
    #make_174_bin_Comp('CompPlotTotalTF',     znn_file, znn_file,"hzvvTF")
    #make_174_bin_Comp('CompPlotYearsLL2018',"inputs/bg_hists/CrossCheck2018/InputsForLimits_data_formatted_LLPlusHadTau_2018.root"  ,"inputs/bg_hists/FullRun2/InputsForLimits_data_formatted_LLPlusHadTau.root","Lost Lepton ", "totalPred_LLPlusHadTau",8.2/137.4)
    #make_174_bin_Comp('CompPlotYearsZ2018',"inputs/bg_hists/CrossCheck2018/ZinvHistos_2018.root"  ,"inputs/bg_hists/FullRun2/ZinvHistos.root","Z( #nu #nu)  ", "ZinvBGpred",8.2/137.4)
    #make_174_bin_Comp('CompPlotHEMLL',"inputs/bg_hists/Run2018Inputs/NoHEM/ZinvHistos.root"  ,"inputs/bg_hists/Run2018Inputs/HEM/ZinvHistos.root","Z( #nu #nu)  ", "hzvvgJNobs",20.92/38.83)
    #make_174_bin_Comp('CompPlotHEMLL',"inputs/bg_hists/Run2018Inputs/NoHEM/InputsForLimits_data_formatted_LLPlusHadTau_PreHEMRecheck.root"  ,"inputs/bg_hists/Run2018Inputs/HEM/InputsForLimits_data_formatted_LLPlusHadTau_PostHEMRecheck.root","LostLept  ", "totalPred_LLPlusHadTau",20.92/38.83)
    #make_174_bin_Comp('CompPlotYearsLL2018',"inputs/bg_hists/CrossCheck2018/InputsForLimits_data_formatted_LLPlusHadTau_2018.root"  ,"inputs/bg_hists/Run2018Inputs/InputsForLimits_data_formatted_LLPlusHadTau_Run2018.root","Lost Lepton ", "totalPred_LLPlusHadTau",8.2/41.5)
    #make_174_bin_CompUnc("CompZGamma2018", "inputs/bg_hists/CrossCheck2018/ZinvHistos_2018.root"  ,"inputs/bg_hists/FullRun2/ZinvHistos.root", " Z/ #gamma ", "hgJZgR", "hgJZgRerr")
    #make_174_bin_CompUnc("CompLLTF2018", "inputs/bg_hists/CrossCheck2018/InputsForLimits_data_formatted_LLPlusHadTau_2018.root"  ,"inputs/bg_hists/FullRun2/InputsForLimits_data_formatted_LLPlusHadTau.root", " 0L/1L ", "LLPlusHadTauTF", "LLPlusHadTauTFErr")
    #make_174_bin_Comp('CompPlotYearsZ',     znn_file, znn_file,"ZinvBGpred")
    #make_174_bin_Comp('CompPlotZgammaRatio',     znn_file, znn_file,"hgJZgR")
    #make_174_bin_Comp('CompPlotDoubleRatio',     znn_file, znn_file,"hZgDR")
    #make_174_bin_Comp('CompPlotPurity',     znn_file, znn_file,"hgJPur")
    #make_174_bin_Comp('CompPlotgJTrig',     znn_file, znn_file,"hgJEtrg")
    #make_174_bin_Comp('CompPlotgJSF',     znn_file, znn_file,"hgJSF")
    #make_174_bin_Comp('CompPlotgJFrag',     znn_file, znn_file,"hgJFdir")
    #make_174_bin_Comp('CompPlotgQcdTail',     znn_file, znn_file,"PredictionCore")
if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    if len(sys.argv) == 1: # no command line inputs -- just use defaults
       make_all_pas_plots_and_tables()
    else:
        make_all_pas_plots_and_tables(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]) #
