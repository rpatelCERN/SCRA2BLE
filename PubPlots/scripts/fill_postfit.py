#!/usr/bin/python

## this is really only here to do the bin combinations
## and to give the data files a structure similar to that of the BG estimation files
## copies the 174 bin data yields from the original data file and makes aggregate predictions

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile
from ROOT import  *

def fill_postfit(inputfile = 'inputs/bg_hists/fitDiagnosticstestCards-allBkgs-T1tttt_2000_200-41.5-mu0.0.root', outputfile = 'postfit_hists.root', nbins = 174):

    print ('Input file is %s' % inputfile)
    print ('Output file is %s' % outputfile)
    print ('Total number of bins is %d' % nbins)

    #TH1D.SetDefaultSumw2(True)
   
    infile = TFile(inputfile,"READ");
    BinProcesses=infile.Get("norm_fit_b");
    hQCDCV = TH1D("hQCDCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hQCDStatUp = TH1D("hQCDStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hQCDStatDown = TH1D("hQCDStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hQCDSysUp = TH1D("hQCDSysUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hQCDSysDown = TH1D("hQCDSysDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5) 
    hZCV = TH1D("hZCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hZStatUp = TH1D("hZStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hZStatDown = TH1D("hZStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hZSysUp = TH1D("hZSysUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hZSysDown = TH1D("hZSysDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5) 
    hWTopCV = TH1D("hWTopCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hWTopStatUp = TH1D("hWTopStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hWTopStatDown = TH1D("hWTopStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hWTopSysUp = TH1D("hWTopSysUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
    hWTopSysDown = TH1D("hWTopSysDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5) 
    for c in range(1,175):
		#sig = BinProcesses.find("ch%d/sig" %c)
		Z   = BinProcesses.find("ch%d/zvv" %c)
		Q   = BinProcesses.find("ch%d/qcd" %c)
		T   = BinProcesses.find("ch%d/WTop" %c)
   		hQCDCV.SetBinContent(c,Q.getVal()); 		
   		hZCV.SetBinContent(c,Z.getVal()); 		
   		hWTopCV.SetBinContent(c,T.getVal()); 		
		 
  		hQCDStatUp.SetBinContent(c,Q.getError()); 		
  		hQCDStatDown.SetBinContent(c,Q.getError()); 		
   		hZStatUp.SetBinContent(c,Z.getError()); 		
   		hZStatDown.SetBinContent(c,Z.getError()); 		
   		hWTopStatUp.SetBinContent(c,T.getError()); 		
   		hWTopStatDown.SetBinContent(c,T.getError()); 		
		 
 		hQCDSysUp.SetBinContent(c,Q.getError()); 		
  		hQCDSysDown.SetBinContent(c,Q.getError()); 		
   		hZSysUp.SetBinContent(c,Z.getError()); 		
   		hZSysDown.SetBinContent(c,Z.getError()); 		
   		hWTopSysUp.SetBinContent(c,T.getError()); 		
   		hWTopSysDown.SetBinContent(c,T.getError()); 		
    outfile = TFile(outputfile, "recreate")
    outfile.cd()
    hQCDCV.Write("QCDCV")
    hZCV.Write("ZinvCV");
    hWTopCV.Write("LLCV")
    hQCDSysUp.Write("QCDSys")
    hZSysUp.Write("ZinvSys");
    hWTopSysUp.Write("LLSys")
    hQCDStatUp.Write("QCDStat")
    hZStatUp.Write("ZinvStat");
    hWTopStatUp.Write("LLStat")

    outfile.Close()


if __name__ == "__main__":
    import sys
    fill_postfit(sys.argv[1], sys.argv[2], int(sys.argv[3]))

