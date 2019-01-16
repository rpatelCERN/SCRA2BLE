from make_1D_projection import make_1D_projection
from make_2D_projection import make_2D_projection


def make_all_1D_projections(lostlept_file = 'lostlept_hists.root', znn_file = 'znn_hists.root', qcd_file = 'qcdrs_hists.root', data_file = 'data_hists.root', signal_file = 'signal_hists.root'):


    ## NJets projection
    make_1D_projection('njets-projection', 'NJ',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, False, True)
    make_1D_projection('njets-projection-pull', 'NJ',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, True, True)
    ## BTags projection
    make_1D_projection('nbjets-projection', 'NB',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 2, H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, False, True)
    make_1D_projection('nbjets-projection-pull', 'NB',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 2, H_{T}^{miss} > 300 GeV, H_{T} > 300 GeV", True, True, True)
    ## MHT projection
    make_1D_projection('mht-projection', 'MHT',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 2, H_{T} > 300 GeV", True, False, True)
    make_1D_projection('mht-projection-pull', 'MHT',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 2, H_{T} > 300 GeV", True, True, True)
    ## HT projection -- work in progress?
    ## make_1D_projection('ht-projection', 'HT',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
    ##                    "T1qqqq_1400_100", "T1qqqq_1000_800", "", True)
    ## make_1D_projection('ht-projection-pull', 'HT',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
    ##                    "T1qqqq_1400_100", "T1qqqq_1000_800", "", True, True)
    ## T1tttt plot: 2+ b-jets, MHT > 500, HT > 500
    make_1D_projection('T1tttt-projection', 'T1tttt',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "N_{b-jet} #geq 2, H_{T}^{miss} > 600 GeV, H_{T} > 700 GeV")
    make_1D_projection('T1tttt-projection-pull', 'T1tttt',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "N_{b-jet} #geq 2, H_{T}^{miss} > 600 GeV, H_{T} > 700 GeV", False, True, True)
    ## T1bbbb plot: 5+ b-jets, MHT > 500, HT > 1000
    make_1D_projection('T1bbbb-projection', 'T1bbbb',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 6, H_{T}^{miss} > 850 GeV, H_{T} > 1700 GeV")
    make_1D_projection('T1bbbb-projection-pull', 'T1bbbb',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 6, H_{T}^{miss} > 850 GeV, H_{T} > 1700 GeV", False, True, True)
    ## T1qqqq plot: 0 b-jets, 5+ jets HT > 1000
    make_1D_projection('T1qqqq-projection', 'T1qqqq',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 6, N_{b-jet} = 0, H_{T} > 1200 GeV")
    make_1D_projection('T1qqqq-projection-pull', 'T1qqqq',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "N_{jet} #geq 6, N_{b-jet} = 0, H_{T} > 1200 GeV", False, True, True)
    ## T2tt plot: 5-8 b-jets, MHT > 500, HT > 500
    make_1D_projection('T2tt-projection', 'T2tt',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2tt_700_50", "T2tt_300_200", "6 #leq N_{jet} #leq 9, H_{T}^{miss} > 600 GeV, H_{T} > 700 GeV")
    make_1D_projection('T2tt-projection-pull', 'T2tt',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2tt_700_50", "T2tt_300_200", "6 #leq N_{jet} #leq 9, H_{T}^{miss} > 600 GeV, H_{T} > 700 GeV", False, True, True)
    ## T2bb plot: 2 b-jets, 2-4 jets, HT > 500
    make_1D_projection('T2bb-projection', 'T2bb',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2bb_650_1", "T2bb_500_300", "2 #leq N_{jet} #leq 5, N_{b-jet} = 2, H_{T} > 700 GeV")
    make_1D_projection('T2bb-projection-pull', 'T2bb',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2bb_650_1", "T2bb_500_300", "2 #leq N_{jet} #leq 5, N_{b-jet} = 2, H_{T} > 700 GeV", False, True, True)
    ## T2qq plot: 0 b-jets, MHT > 500, HT > 500
    make_1D_projection('T2qq-projection', 'T2qq',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2qq_1000_100", "T2qq_700_400", "N_{b-jet} = 0, H_{T}^{miss} > 850 GeV, H_{T} > 1200 GeV")
    make_1D_projection('T2qq-projection-pull', 'T2qq',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2qq_1000_100", "T2qq_700_400", "N_{b-jet} = 0, H_{T}^{miss} > 850 GeV, H_{T} > 1200 GeV", False, True, True)

    ## 2D plots with signal stacked on BG
    make_2D_projection('2D-T1tttt', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV")
    make_2D_projection('2D-T1bbbb', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV")
    make_2D_projection('2D-T1qqqq', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV")
    make_2D_projection('2D-T2tt', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2tt_700_50", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV")
    make_2D_projection('2D-T2bb', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2bb_650_1", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV")
    make_2D_projection('2D-T2qq', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2qq_1000_100", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV")
    make_2D_projection('2D-T1tttt-pull', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV", doPull=True)
    make_2D_projection('2D-T1bbbb-pull', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV", doPull=True)
    make_2D_projection('2D-T1qqqq-pull', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV", doPull=True)
    make_2D_projection('2D-T2tt-pull', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2tt_700_50", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV", doPull=True)
    make_2D_projection('2D-T2bb-pull', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2bb_650_1", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV", doPull=True)
    make_2D_projection('2D-T2qq-pull', '2D',  lostlept_file, znn_file, qcd_file, data_file, signal_file, \
                       "T2qq_1000_100", "H_{T}^{miss} > 850 GeV, H_{T} > 850 GeV", doPull=True)

if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    if len(sys.argv) == 1: # no command line inputs -- just use defaults
        make_all_1D_projections()
    else:
        make_all_1D_projections(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]) #
