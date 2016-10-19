#!/usr/bin/python

## this is really only here to do the bin combinations
## and to give the data files a structure similar to that of the BG estimation files
## copies the 160 bin data yields from the original data file and makes aggregate predictions

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile
from data_obs import DataObs
from agg_bins import *

def fill_data_hists(inputfile = 'inputs/data_hists/Data_160Bins_SR_Approval_12.9.root', outputfile = 'data_hists.root', nbins = 160):

    print ('Input file is %s' % inputfile)
    print ('Output file is %s' % outputfile)
    print ('Total number of bins is %d' % nbins)

    TH1D.SetDefaultSumw2(True)
   
    infile = TFile.Open(inputfile);
    data_obs = DataObs(infile.Get("data"))

    outfile = TFile(outputfile, "recreate")
    outfile.cd()
    data_obs.hist.Write()
    data_obs.graph.Write()

    for name, asrs in asr_sets.items():
        dASR = outfile.mkdir(name)
        dASR.cd()
        data_obs_asr = data_obs.AggregateBins(asrs, asr_xtitle[name], asr_xbins[name])
        data_obs_asr.hist.Write()
        data_obs_asr.graph.Write()

    outfile.Close()


if __name__ == "__main__":
    import sys
    fill_data_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))

