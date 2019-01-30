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

def fill_znn_hists(inputfile = 'inputs/bg_hists/ZinvHistos.root', outputfile = 'znn_hists.root', nbins = 174, lumiSF=1.):
   
   print ('Input file is %s' % inputfile)
   print ('Output file is %s' % outputfile)
   print ('Total number of bins is %d' % nbins)

   TH1D.SetDefaultSumw2(True)
   
   infile = TFile.Open(inputfile)
   hin = infile.Get("ZinvBGpred")
   hin_CR = infile.Get("hzvvgJNobs")
   hin_TF = infile.Get("hzvvTF")

   # and load input systematics
   SYSTS = []
   SYSTS_Up = []
   SYSTS_Down = []
   for h in infile.GetListOfKeys():
       h = h.ReadObj()
       # skip the histograms that don't actually contain systematics -- make sure you check the names haven't changed
       if h.GetName().find('hzvv') < 0 \
         or h.GetName() == 'hzvvgJNobs' \
         or h.GetName() == 'hzvvTF':
           continue
       # convert to absolute
       print(h.GetName())
       hout = h.Clone()
       hout.Reset() 
       for ibin in range(nbins):
           if hin.GetBinContent(ibin+1) > 0.:
               if hout.GetName().find("Low") >= 0:
                   hout.SetBinContent(ibin+1, lumiSF*(1.-h.GetBinContent(ibin+1))*hin.GetBinContent(ibin+1))
               else:
                   hout.SetBinContent(ibin+1, lumiSF*(h.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1))
           else:
               hout.SetBinContent(ibin+1, 0.)            
           ## note: it appears we no longer need to assign gJets syst from NB = 0 to corresponding bins with NB > 0 -- already filled in
       SYSTS.append(hout)
       if hout.GetName().find('Low') >= 0:
           SYSTS_Down.append(hout)
           print("%s (down-only): %3.2f" % (hout.GetName(), hout.GetBinContent(161)))       
       elif hout.GetName().find('Up') >= 0:
           SYSTS_Up.append(hout)
           print("%s (up-only): %3.2f" % (hout.GetName(), hout.GetBinContent(161)))       
       else:
           SYSTS_Up.append(hout)
           SYSTS_Down.append(hout)
           print("%s (sym): %3.2f" % (hout.GetName(), hout.GetBinContent(161)))       

   hSystUp = AddHistsInQuadrature('hSystUp', SYSTS_Up)       
   hSystDown = AddHistsInQuadrature('hSystDown', SYSTS_Down)
   
   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stata and syst uncertainties in these histograms
   hCV = TH1D("hCV", "Search region bin number;Events", nbins, 0.5, nbins + 0.5)
   hStatUp = TH1D("hStatUp", "Search region bin number;Events", nbins, 0.5, nbins + 0.5)
   hStatDown = TH1D("hStatDown", "Search region bin number;Events", nbins, 0.5, nbins + 0.5)
   
   # open text file, extract values
   if nbins != hin.GetNbinsX():
       print ('Warning: input file has %d bins, but I need to fill %d bins!' % (hin.GetNbinsX(), nbins))
   for ibin in range(nbins):
       CV = lumiSF*hin.GetBinContent(ibin+1)
       hCV.SetBinContent(ibin+1, CV)
       hCV.SetBinError(ibin+1, 0.)
       # get stat uncertainties
       NCR = hin_CR.GetBinContent(ibin+1)
       L = 0.
       if NCR > 0.:
           L = Math.gamma_quantile(alpha/2,NCR,1.)
       U = Math.gamma_quantile_c(alpha/2,NCR+1,1.)
       stat_up = lumiSF*(U-NCR)*hin_TF.GetBinContent(ibin+1)
       hStatUp.SetBinContent(ibin+1, stat_up)
       stat_down = lumiSF*(NCR-L)*hin_TF.GetBinContent(ibin+1)
       if stat_down > CV: # for some reason, this one is sometimes greater than the central value, so truncate
           stat_down = CV
       hStatDown.SetBinContent(ibin+1, stat_down)
       if hSystDown.GetBinContent(ibin+1) > sqrt(CV**2 - hStatDown.GetBinContent(ibin+1)**2): # truncate if necessary
           hSystDown.SetBinContent(ibin+1, sqrt(CV**2 - hStatDown.GetBinContent(ibin+1)**2))
       print ('Bin %d: %f + %f + %f - %f - %f' % (ibin+1, CV, hStatUp.GetBinContent(ibin+1), hSystUp.GetBinContent(ibin+1), hStatDown.GetBinContent(ibin+1), hSystDown.GetBinContent(ibin+1)))
           
             
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
           correlation = 'all' # note:default is fully-correlated, corresponds to ScaleErr, photon purity
           if hsyst.GetName() == 'hzvvDYsysKin':
               correlation = ''
           elif hsyst.GetName().find('hzvvNbCorrel') >= 0: # DR, fragmentation factor
               correlation = 'nbjets'
           elif hsyst.GetName().find('hzvvgJEtrgErr') >= 0: # trigger efficiency, binned in MHT
               correlation = 'njets:nbjets'
           elif hsyst.GetName().find('DYstat') >= 0: # special
               correlation = 'DYstat'
           elif hsyst.GetName().find('zvvDYMCerr') >= 0 or hsyst.GetName().find('hzvvDYsysNj') >= 0: # 3 values for nb = 1, 2, 3 for njets>8
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
   
