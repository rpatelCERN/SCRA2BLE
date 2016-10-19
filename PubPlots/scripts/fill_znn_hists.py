#!/usr/bin/python
## take data-driven Z-->inv estimation from Bill's file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math
from uncertainty import Uncertainty
from agg_bins import *

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

   # and load input systematics
   SYSTS = []
   for h in infile.GetListOfKeys():
       h = h.ReadObj()
       # skip the histograms that don't actually contain systematics -- make sure you check the names haven't changed
       if (h.GetName().find('hgJ') == 0 and not (h.GetName().find('hgJPurErr') == 0 or h.GetName().find('hgJZgRdataMCerr') == 0)) \
         or (h.GetName().find('hDYvalue') == 0) \
         or (h.GetName().find('Zinv') >= 0 and not h.GetName().find('hZinvScaleErr') == 0):
           continue
       # print( h.GetName())
       # convert to absolute
       hout = h.Clone()
       hout.Reset() 
       for ibin in range(nbins):
           if (h.GetName().find('hgJ') == 0 or h.GetName() == 'hZinvScaleErr') and SearchBin(ibin+1).inb > 0: # assign gJets syst from NB = 0 to corresponding bins with NB > 0
               # print(h.GetName(), ibin+1, SearchBin(ibin+1).inj*40+SearchBin(ibin+1).ihtmht+1)
               hout.SetBinContent(ibin+1, h.GetBinContent(SearchBin(ibin+1).inj*40+SearchBin(ibin+1).ihtmht+1)*hin.GetBinContent(ibin+1)) 
           else:
               hout.SetBinContent(ibin+1, h.GetBinContent(ibin+1)*hin.GetBinContent(ibin+1))
       SYSTS.append(hout)

   
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
       ## print ('Bin %d: %f + %f + %f - %f - %f' % (ibin+1, CV, hStatUp.GetBinContent(ibin+1), hSystUp.GetBinContent(ibin+1), hStatDown.GetBinContent(ibin+1), hSystDown.GetBinContent(ibin+1)))
           
             
   outfile.cd()
   hCV.Write()
   hStatUp.Write()
   hStatDown.Write()
   hSystUp.Write()
   hSystDown.Write()

   # and now for aggregate bin predicitons
   for name, asrs in asr_sets.items():
       dASR = outfile.mkdir(name)
       dASR.cd()
       hCV_ASR = Uncertainty(hCV, "all").AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist # pretending the CV is a fully-correlated uncertainty b/c we need to add it linearly
       ## CR not binned in nbjets, so stat err on bins with same htmht & njets are correlated
       hStatUp_ASR = Uncertainty(hStatUp, 'nbjets').AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist 
       hStatDown_ASR = Uncertainty(hStatDown, 'nbjets').AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
       hCV_ASR.Write()
       
       SYSTSUp_ASR = []
       SYSTSDown_ASR = []
       for hsyst in SYSTS:
           correlation = 'all' # note:default is fully-correlated, corresponds to ZinvScaleErr, gJPurErr, and DYsysNj
           if hsyst.GetName() == 'hDYsysKin':
               correlation = ''
           elif hsyst.GetName().find('gJZgRdataMCerr') >= 0: # hgJZgRdataMCerrUp, hgJZgRdataMCerrLow
               correlation = 'nbjets'
           elif hsyst.GetName().find('stat') >= 0: # DYstat, DYMCstat
               correlation = 'htmht'
           elif hsyst.GetName().find('DYsysPur') >= 0: # funny
               correlation = 'DYsysPur'
           ## Up, Low, Sym
           hist_asr = Uncertainty(hsyst, correlation).AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
           if hsyst.GetName().find('Low') >= 0:
               SYSTSDown_ASR.append(hist_asr)            
           elif hsyst.GetName().find('Up') >= 0:
               SYSTSUp_ASR.append(hist_asr)
           else:
               SYSTSUp_ASR.append(hist_asr)
               SYSTSDown_ASR.append(hist_asr)
               
       hSystUp_ASR = AddHistsInQuadrature('hSystUp', SYSTSUp_ASR)       
       hSystDown_ASR = AddHistsInQuadrature('hSystDown', SYSTSDown_ASR)
       # sanity: make sure Stat and Syst Down not larger than CV
       for iasr in range(hCV_ASR.GetNbinsX()):
           CV_asr = hCV_ASR.GetBinContent(iasr+1)
           stat_down_asr = hStatDown_ASR.GetBinContent(iasr+1)
           syst_down_asr = hSystDown_ASR.GetBinContent(iasr+1)
           # print ("ASR %d: %f - %f - %f" % (iasr+1, CV_asr, stat_down_asr, syst_down_asr))
           if stat_down_asr > CV_asr:
               stat_down_asr = CV_asr
               hStatDown_ASR.SetBinContent(iasr+1, stat_down_asr)
           if syst_down_asr > CV_asr - stat_down_asr:
               hSystDown_ASR.SetBinContent(iasr+1, CV_asr - stat_down_asr)
       hStatUp_ASR.Write()
       hSystUp_ASR.Write()
       hStatDown_ASR.Write()
       hSystDown_ASR.Write()
   
   outfile.Close()
        
if __name__ == "__main__":
    import sys
    fill_znn_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
   
