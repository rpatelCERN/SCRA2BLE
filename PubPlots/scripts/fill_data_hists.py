#!/usr/bin/python

## this is really only here to do the bin combinations
## and to give the data files a structure similar to that of the BG estimation files
## copies the 174 bin data yields from the original data file and makes aggregate predictions

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile
from data_obs import DataObs
from agg_bins import *

def fill_data_hists(inputfile = 'inputs/data_hists/RA2bin_signal.root', inputhist = 'RA2bin_data', outputfile = 'data_hists.root', nbins = 174):

    print ('Input file is %s' % inputfile)
    print ('Output file is %s' % outputfile)
    print ('Total number of bins is %d' % nbins)

    TH1D.SetDefaultSumw2(True)
   
    infile = TFile.Open(inputfile);
    infile2 = TFile.Open("inputs/data_hists/data_althemveto/RA2bin_signal.root", "READ");
    dataTotal=infile.Get(inputhist)
    dataTotal.Add(infile.Get("RA2bin_data2017"))
    dataTotal.Add(infile.Get("RA2bin_data2018"))
    dataTotal.Add(infile.Get("RA2bin_data2018HEM"))
    #dataTotal.Add(infile2.Get("RA2bin_data2018HEM_ra2bin2018HEM-alt2"))
    data_obs = DataObs(dataTotal)
   
    outfile = TFile(outputfile, "recreate")
    outfile.cd()
    data_obs.hist.Write()
    data_obs.graph.Write()

    for name, asrs in asr_sets.items():
        print(name)
        dASR = outfile.mkdir(name)
        dASR.cd()
        verbose=False
        if name=='ASR': verbose=True
        data_obs_asr = data_obs.AggregateBins(asrs, asr_xtitle[name], asr_xbins[name], verbose)
        data_obs_asr.hist.Write()
        data_obs_asr.graph.Write()

    outfile.Close()


if __name__ == "__main__":
    import sys
    fill_data_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))

