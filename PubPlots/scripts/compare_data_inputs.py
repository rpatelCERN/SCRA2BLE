#!/usr/bin/python

## compare my data inputs to Kevin's

from __future__ import print_function

from ROOT import TFile, TH1

def compare_data_inputs(file1, hist1, file2, hist2):

    print ('File 1: %s' % file1)
    print ('File 2: %s' % file2)

    
    print ('File 1 - File2: ')

    TH1.SetDefaultSumw2(True)
   
    infile1 = TFile.Open(file1);
    infile2 = TFile.Open(file2);
    h1 = infile1.Get(hist1)
    h2 = infile2.Get(hist2)


    if h1.GetNbinsX()-h2.GetNbinsX() != 0:
        print("Error: historgrams have different numbers of bins!")
        return -1
    
    for ibin in range(h1.GetNbinsX()):
        if h1.GetBinContent(ibin+1)-h2.GetBinContent(ibin+1) != 0.:
            print("Bin %d: %3.0f" % (ibin+1, h1.GetBinContent(ibin+1)-h2.GetBinContent(ibin+1)))


if __name__ == "__main__":
    import sys
    compare_data_inputs(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

