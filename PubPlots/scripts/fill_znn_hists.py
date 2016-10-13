#!/usr/bin/python
## take data-driven Z-->inv estimation from Bill's file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math

alpha = 1 - 0.6827

def fill_znn_hists(inputfile = 'inputs/bg_hists/ZinvHistos.root', outputfile = 'inputs/bg_hists/znn_hists.root', nbins = 160):
   
   print ('Input file is %s' % inputfile)
   print ('Output file is %s' % outputfile)
   print ('Total number of bins is %d' % nbins)

   TH1D.SetDefaultSumw2(True)
   
   infile = TFile.Open(inputfile);
   hin = infile.Get("ZinvBGpred");
   hin_systup = infile.Get("ZinvBGsysUp");
   hin_0evt_statup = infile.Get("ZinvBG0EVsysUp");
   hin_systdown = infile.Get("ZinvBGsysLow");

   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stata and syst uncertainties in these histograms
   hCV = TH1D("hCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatUp = TH1D("hStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatDown = TH1D("hStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystUp = TH1D("hSystUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystDown = TH1D("hSystDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   
   # open text file, extract values
   if nbins != hin.GetNbinsX():
       print ('Warning: input file has %d bins, but I need to fill %d bins!' % (hin.GetNbinsX(), nbins))
   for ibin in range(nbins):
       CV = hin.GetBinContent(ibin+1)
       hCV.SetBinContent(ibin+1, CV)
       hCV.SetBinError(ibin+1, 0.)
       # get stat uncertainties
       stat_up = hin.GetBinError(ibin+1);
       if stat_up==0.:
           stat_up = hin_0evt_statup.GetBinError(ibin+1)
       hStatUp.SetBinContent(ibin+1, stat_up)
       stat_down = hin.GetBinError(ibin+1)
       if stat_down > CV: # for some reason, this one is sometimes greater than the central value, so truncate
           stat_down = CV
       hStatDown.SetBinContent(ibin+1, stat_down)
       # get syst uncertainties
       syst_up = hin_systup.GetBinContent(ibin+1)
       syst_down = hin_systdown.GetBinContent(ibin+1)
       if syst_down > CV - hStatDown.GetBinContent(ibin+1): # truncate if necessary
           syst_down = CV - hStatDown.GetBinContent(ibin+1)
       hSystUp.SetBinContent(ibin+1, syst_up)
       hSystDown.SetBinContent(ibin+1, syst_down)
       print ('Bin %d: %f + %f + %f - %f - %f' % (ibin+1, CV, hStatUp.GetBinContent(ibin+1), hSystUp.GetBinContent(ibin+1), hStatDown.GetBinContent(ibin+1), hSystDown.GetBinContent(ibin+1)))
           
             
   outfile.cd()
   hCV.Write()
   hStatUp.Write()
   hStatDown.Write()
   hSystUp.Write()
   hSystDown.Write()
   outfile.Close()
        
if __name__ == "__main__":
    import sys
    fill_znn_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
   
