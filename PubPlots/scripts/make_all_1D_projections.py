from make_1D_projection import make_1D_projection


def make_all_1D_projections(lostlep_file = 'lostlep_hists.root', hadtau_file = 'hadtau_hists.root', znn_file = 'znn_hists.root', qcd_file = 'qcd_hists.root', data_file = 'data_hists.root', signal_file = 'signal_hists.root'):


    ## NJets projection
    make_1D_projection('njets-projection', 'NJ', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "", True)
    make_1D_projection('njets-projection-pull', 'NJ', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "", True, True)
    ## BTags projection
    make_1D_projection('nbjets-projection', 'NB', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "", True)
    make_1D_projection('nbjets-projection-pull', 'NB', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "", True, True)
    ## MHT projection
    make_1D_projection('mht-projection', 'MHT', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "", True)
    make_1D_projection('mht-projection-pull', 'MHT', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1qqqq_1400_100", "T1qqqq_1000_800", "", True, True)
    ## T1tttt plot: 2+ b-jets, MHT > 500, HT > 500
    make_1D_projection('t1tttt-projection-njets-nb2-mht500-ht500', 'NJ_NB2toInf_MHT500_HT500', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "N_{b-jet} #geq 2, H_{T}^{miss} > 500 GeV, H_{T} > 500 GeV")
    make_1D_projection('t1tttt-projection-njets-nb2-mht500-ht500-pull', 'NJ_NB2toInf_MHT500_HT500', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1tttt_1500_100", "T1tttt_1200_800", "N_{b-jet} #geq 2, H_{T}^{miss} > 500 GeV, H_{T} > 500 GeV", False, True)
    ## T1bbbb plot: 2+ b-jets, MHT > 500, HT > 500
    make_1D_projection('t1bbbb-projection-nbjets-nj5-mht500-ht1000', 'NB_NJ5toInf_MHT500_HT1000', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 5, H_{T}^{miss} > 500 GeV, H_{T} > 1000 GeV")
    make_1D_projection('t1bbbb-projection-nbjets-nj5-mht500-ht1000-pull', 'NB_NJ5toInf_MHT500_HT1000', lostlep_file, hadtau_file, znn_file, qcd_file, data_file, signal_file, \
                       "T1bbbb_1500_100", "T1bbbb_1000_900", "N_{jet} #geq 5, H_{T}^{miss} > 500 GeV, H_{T} > 1000 GeV", False, True)

    
if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    make_all_1D_projections(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]) # 
