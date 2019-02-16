#!/usr/bin/python
## take data-driven QCD R+S estimation from San's file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
from math import sqrt
from ROOT import TFile, TH1D, Math, TProfile, gDirectory
from uncertainty import Uncertainty
from agg_bins import *

alpha = 1 - 0.6827

def fill_qcdrs_hists(inputfile = 'inputs/bg_hists/QcdPredictionRandS_35.9.root', outputfile = 'qcdrs_hists.root', nbins = 174, lumiSF = 1.):

   print ('Input file is %s' % inputfile)
   print ('Output file is %s' % outputfile)
   print ('Total number of bins is %d' % nbins)

   TH1D.SetDefaultSumw2(True)

   infile = TFile.Open(inputfile);
   hin = infile.Get("PredictionCV");
   hstat = infile.Get("hStat")
   #hstat = infile.Get("PredictionUncorrelated")
   #hstat = infile.Get("hPredictionUncorrelated")

   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stat and syst uncertainties in these histograms
   hCV = TH1D("hCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatUp = TH1D("hStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatDown = TH1D("hStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)

   ## load systematics from input hists
   SYSTS = []
   SYSTS_Up = []
   SYSTS_Down = []
   for h in infile.GetListOfKeys():
       h = h.ReadObj()
       # skip the histograms that don't actually contain systematics -- make sure you check the names haven't changed
       if h.GetName().find('CV') >= 0 or h.GetName().find('Stat') >= 0 or h.GetName().find('hBaseline_SearchBinsRplusS')>=0:
           continue
       print(h.GetName())
       # convert to absolute
       hout = h.Clone()
       hout.Reset()
       for ibin in range(nbins):
           if hin.GetBinContent(ibin+1) > 0.:
               if hout.GetName().find("Down") >= 0:
                   hout.SetBinContent(ibin+1, lumiSF*(1.-h.GetBinContent(ibin+1))*hin.GetBinContent(ibin+1))
               else:
                   hout.SetBinContent(ibin+1, lumiSF*(h.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1))
           else:
               hout.SetBinContent(ibin+1, 0.)
       SYSTS.append(hout)
       if hout.GetName().find('Down') >= 0:
           SYSTS_Down.append(hout)
           print("%s (down-only)" % (hout.GetName()))
       elif hout.GetName().find('Up') >= 0 and "Core" not in hout.GetName() and "Tail" not in hout.GetName():
           SYSTS_Up.append(hout)
           print("%s (up-only)" % (hout.GetName()))
       else:
           SYSTS_Up.append(hout)
           SYSTS_Down.append(hout)
           print("%s (sym)" % hout.GetName())

   hSystUp = AddHistsInQuadrature('hSystUp', SYSTS_Up)
   hSystDown = AddHistsInQuadrature('hSystDown', SYSTS_Down)

   # open text file, extract values
   if nbins != hin.GetNbinsX():
       print ('Warning: input file has %d bins, but I need to fill %d bins!' % (hin.GetNbinsX(), nbins))
   for ibin in range(nbins):
       CV = lumiSF*hin.GetBinContent(ibin+1)
       hCV.SetBinContent(ibin+1, CV)
       hCV.SetBinError(ibin+1, 0.)
       # get stat uncertainties
       stat = (hstat.GetBinContent(ibin+1)-1.)*CV;
       hStatUp.SetBinContent(ibin+1, stat)
       if stat > CV: # just to be safe
           hStatDown.SetBinContent(ibin+1, CV)
       else:
           hStatDown.SetBinContent(ibin+1, stat)
       ## truncate -SYST if necessary
       if hSystDown.GetBinContent(ibin+1) > CV - hStatDown.GetBinContent(ibin+1): # truncate if necessary
           hSystDown.SetBinContent(ibin+1, CV - hStatDown.GetBinContent(ibin+1))
       print ('Bin %d: %f + %f + %f - %f - %f' % (ibin+1, CV, hStatUp.GetBinContent(ibin+1), hSystUp.GetBinContent(ibin+1), hStatDown.GetBinContent(ibin+1), hSystDown.GetBinContent(ibin+1)))



   outfile.cd()
   hCV.Write()
   hStatUp.Write()
   hStatDown.Write()
   hSystUp.Write()
   hSystDown.Write()


   outfile.cd()
   # and now for aggregate bin predicitons
   for name, asrs in asr_sets.items():
       dASR = outfile.mkdir(name)
       dASR.cd()
       hCV_ASR = Uncertainty(hCV, "all").AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist # pretending the CV is a fully-correlated uncertainty b/c we need to add it linearly
       # stat uncertainty fully-uncorrelated (174 CRs)
       hStatUp_ASR = Uncertainty(hStatUp, '').AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
       hStatDown_ASR = Uncertainty(hStatDown, '').AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
       hCV_ASR.Write()

       SYSTSUp_ASR = []
       SYSTSDown_ASR = []
       for hsyst in SYSTS:
           hname = hsyst.GetName()
           correlation = '' # note: default is uncorrelated across bins corresponds to closure, contamination, trigger, prior
           if hname.find('Core') >= 0 or hname.find('Tail') >= 0 or hname.find('BTag') >= 0: # fully-correlated across search bins
               correlation = 'all'
           hist_asr = Uncertainty(hsyst, correlation).AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
           ## now group by Up, Down, symmetric
           if hname.find('Down') >= 0:
               SYSTSDown_ASR.append(hist_asr)
           elif hname.find('Up') >= 0:
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
       dASR.cd()
       hStatUp_ASR.Write()
       hSystUp_ASR.Write()
       hStatDown_ASR.Write()
       hSystDown_ASR.Write()

   outfile.Close()

if __name__ == "__main__":
    import sys
    fill_qcdrs_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
