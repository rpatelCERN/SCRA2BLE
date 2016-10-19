#!/usr/bin/python

## make the aggregate bin histograms for signal, using the DataObs class to do the aggregating
## see fill_signal_hists for instructions on how to add more signal models
## note that this will produce signal histograms scaled to 1 pb-1
## you'll have to scale them to a given luminosity in the plotting scripts

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile
from data_obs import DataObs
from signal_model import SignalModel
from agg_bins import *

def fill_signal_hists(outputfile = 'signal_hists.root', nbins = 160):

    print ('Output file is %s' % outputfile)
    print ('Total number of bins is %d' % nbins)

    TH1D.SetDefaultSumw2(True)

    outfile = TFile(outputfile, "recreate")
    outfile.cd()

    ## if you want to make histograms for any other models,
    ## just add them to this list
    signal_models = [SignalModel("T1tttt", 1500, 100), SignalModel("T1tttt", 1200, 800), \
                     SignalModel("T1bbbb", 1500, 100), SignalModel("T1bbbb", 1000, 900), \
                     SignalModel("T1qqqq", 1400, 100), SignalModel("T1qqqq", 1000, 800), \
                     SignalModel("T2tt", 700, 50), SignalModel("T2tt", 300, 200), \
                     SignalModel("T2bb", 650, 1), SignalModel("T2bb", 500, 300), \
                     SignalModel("T2qq", 1000, 100), SignalModel("T2qq", 700, 400), \
                     SignalModel("T5qqqqVV", 1400, 100), SignalModel("T5qqqqVV", 1000, 800)]
                     
    for name, asrs in asr_sets.items():
        dASR = outfile.mkdir(name)
        dASR.cd()
        for model in signal_models:
            inhist = model.inhist
            asr_hist = model.AggregateBins(asrs, asr_xtitle[name], asr_xbins[name])
            # do some standard formatting -- does not set line style
            asr_hist.SetLineWidth(3)
            asr_hist.SetLineColor(4)
            asr_hist.SetFillColor(0)
            asr_hist.SetMarkerSize(0)
            asr_hist.Write()
        
    outfile.Close()


if __name__ == "__main__":
    import sys
    fill_signal_hists(sys.argv[1], int(sys.argv[2]))

