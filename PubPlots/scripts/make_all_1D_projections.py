from make_1D_projection import make_1D_projection
from make_2D_projection import make_2D_projection


def make_all_1D_projections(lostlep_file = 'lostlep_hists.root', hadtau_file = 'hadtau_hists.root', znn_file = 'znn_hists.root', qcd_file = 'qcdrs_hists.root', data_file = 'data_hists.root', signal_file = 'signal_hists.root'):


    ## NJets projection
    make_1D_projection('njets-projection', 'NJ', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True)
    make_1D_projection('njets-projection-pull', 'NJ', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, True)
    ## BTags projection
    make_1D_projection('nbjets-projection', 'NB', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 2, H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True)
    make_1D_projection('nbjets-projection-pull', 'NB', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 2, H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, True)
    ## MHT projection
    make_1D_projection('mht-projection', 'MHT', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 2, H_{T} > 300 GeV", True)
    make_1D_projection('mht-projection-pull', 'MHT', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 2, H_{T} > 300 GeV", True, True)
    ## HT projection -- work in progress?
    ## make_1D_projection('ht-projection', 'HT', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
    ##                    "T1qqqq_1400_100", "T1qqqq_1000_800", "", True)
    ## make_1D_projection('ht-projection-pull', 'HT', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
    ##                    "T1qqqq_1400_100", "T1qqqq_1000_800", "", True, True)
    ## T1tttt plot: 2+ b-jets, MHT > 500, HT > 500
    make_1D_projection('T1tttt-projection', 'T1tttt', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "N_{b-jet} #geq 2, H_{T}^{miss} > 500 GeV, H_{T} > 500 GeV")
    make_1D_projection('t1tttt-projection-njets-nb2-mht500-ht500-pull', 'T1tttt', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "N_{b-jet} #geq 2, H_{T}^{miss} > 500 GeV, H_{T} > 500 GeV", False, True)
    ## T1bbbb plot: 5+ b-jets, MHT > 500, HT > 1000
    make_1D_projection('T1bbbb-projection', 'T1bbbb', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 5, H_{T}^{miss} > 750 GeV, H_{T} > 1500 GeV")
    make_1D_projection('t1bbbb-projection-nbjets-nj5-mht750-ht1500-pull', 'T1bbbb', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 5, H_{T}^{miss} > 750 GeV, H_{T} > 1500 GeV", False, True)
    ## T1qqqq plot: 0 b-jets, 5+ jets HT > 1000
    make_1D_projection('T1qqqq-projection', 'T1qqqq', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 5, N_{b-jet} = 0, H_{T} > 1000 GeV")
    make_1D_projection('t1qqqq-projection-mht-nj5-nb0-ht1000-pull', 'T1qqqq', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 5, N_{b-jet} = 0, H_{T} > 1000 GeV", False, True)
    ## T2tt plot: 5-8 b-jets, MHT > 500, HT > 500
    make_1D_projection('T2tt-projection', 'T2tt', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2tt_700_50", "T2tt_300_200", "5 #leq N_{jet} #leq 8, H_{T}^{miss} > 500 GeV, H_{T} > 500 GeV")
    make_1D_projection('t2tt-projection-nbjets-nj5to8-mht500-ht500-pull', 'T2tt', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2tt_700_50", "T2tt_300_200", "5 #leq N_{jet} #leq 8, H_{T}^{miss} > 500 GeV, H_{T} > 500 GeV", False, True)
    ## T2bb plot: 2 b-jets, 2-4 jets, HT > 500
    make_1D_projection('T2bb-projection', 'T2bb', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2bb_650_1", "T2bb_500_300", "2 #leq N_{jet} #leq 4, N_{b-jet} = 2, H_{T} > 500 GeV")
    make_1D_projection('t2bb-projection-mht-nj2to4-nb2-ht500-pull', 'T2bb', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2bb_650_1", "T2bb_500_300", "2 #leq N_{jet} #leq 4, N_{b-jet} = 2, H_{T} > 500 GeV", False, True)
    ## T2qq plot: 0 b-jets, MHT > 500, HT > 500
    make_1D_projection('T2qq-projection', 'T2qq', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2qq_1000_100", "T2qq_700_400", "N_{b-jet} = 0, H_{T}^{miss} > 750 GeV, H_{T} > 1000 GeV")
    make_1D_projection('t2qq-projection-njets-nb0-mht750-ht1000-pull', 'T2qq', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2qq_1000_100", "T2qq_700_400", "N_{b-jet} = 0, H_{T}^{miss} > 750 GeV, H_{T} > 1000 GeV", False, True)

    ## 2D plots with signal stacked on BG
    make_2D_projection('2D-T1tttt', '2D', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "H_{T}^{miss} > 750 GeV, H_{T} > 750 GeV")
                       
if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    if len(sys.argv) == 1: # no command line inputs -- just use defaults
        make_all_1D_projections()
    else:
        make_all_1D_projections(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]) # 
