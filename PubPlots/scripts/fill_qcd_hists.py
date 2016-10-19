#!/usr/bin/python
## take data-driven QCD estimation from text file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math, TDirectory
from bg_est import BGEst
from uncertainty import Uncertainty
from agg_bins import *

alpha = 1 - 0.6827

def fill_qcd_hists(inputfile = 'inputs/bg_hists/qcd-bg-combine-input-12.9ifb-july28-nodashes.txt', outputfile = 'qcd_hists.root', nbins = 160):
      

   print ('Input file is %s' % inputfile)
   print ('Output file is %s' % outputfile)
   print ('Total number of bins is %d' % nbins)

   TH1D.SetDefaultSumw2(True)
   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stata and syst uncertainties in these histograms
   hCV = TH1D("hCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatUp = TH1D("hStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatDown = TH1D("hStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystUp = TH1D("hSystUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystDown = TH1D("hSystDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)

   hNonQCDErr = TH1D("hNonQCDErr", ";Search Bin;Fractional syst.", nbins, 0.5, nbins + 0.5);
   ## for ibin in range(nbins): # sert default to 1 -- no uncertainty
   ##     hNonQCDErr.SetBinContent(ibin+1,1.)
   SYSTS = [hNonQCDErr, hNonQCDErr.Clone("hKHT1"), hNonQCDErr.Clone("hKHT2"), hNonQCDErr.Clone("hKHT3"), \
            hNonQCDErr.Clone("hSNJ2"), hNonQCDErr.Clone("hSNJ3"), hNonQCDErr.Clone("hSNJ4"), \
            hNonQCDErr.Clone("hSH1M1"), hNonQCDErr.Clone("hSH1M2"), \
            hNonQCDErr.Clone("hSH2M1"), hNonQCDErr.Clone("hSH2M2"), hNonQCDErr.Clone("hSH2M3"), hNonQCDErr.Clone("hSH2M4"), \
            hNonQCDErr.Clone("hSH3M1"), hNonQCDErr.Clone("hSH3M2"), hNonQCDErr.Clone("hSH3M3"), hNonQCDErr.Clone("hSH3M4"), \
            hNonQCDErr.Clone("hMCC")]
   
   
   # open text file, extract values
   with open(inputfile) as fin:
       num_lines = sum(1 for line in fin)
       ibin = -1
       if nbins+1 != num_lines:
           print ('Warning: text file has %d lines, but I need to fill %d bins!' % (num_lines, nbins))
       fin.seek(0)
       for line in fin:
           ibin = ibin+1
           if ibin < 1:
               continue
           values = line.split()
           if len(values) != 32:
               print ('Warning: this line looks funny')
           CV = abs(max(float(values[len(values)-3]), 0.))
           hCV.SetBinContent(ibin, CV)
           hCV.SetBinError(ibin, 0.)
           # get stat uncertainties from CR observation - EWK contamination
           NLDP = float(values[2])
           RQCD = float(values[6])
           N_nonQCD = float(values[3])
           NCR = max(NLDP-N_nonQCD, 0.)
           L = 0.
           if NCR > 0.:
               L = Math.gamma_quantile(alpha/2,NCR,1.)
           U = Math.gamma_quantile_c(alpha/2,NCR+1,1.)
           hStatUp.SetBinContent(ibin,RQCD*(U-NCR))
           hStatDown.SetBinContent(ibin,RQCD*(NCR-L))
           err_nonQCD = max(RQCD*float(values[5]), 0.)
           syst = 0.
           if CV > 0.:
               syst = syst + pow(err_nonQCD, 2.)
               hNonQCDErr.SetBinContent(ibin, err_nonQCD) 
               for isyst in range(8, len(values)-7):
                   # print ("isyst: ", isyst)
                   syst = syst + pow((float(values[isyst])-1.)*CV, 2.)
                   SYSTS[isyst-7].SetBinContent(ibin, (float(values[isyst])-1.)*CV)
               syst = math.sqrt(syst)
           hSystUp.SetBinContent(ibin, syst)
           if syst > CV - hStatDown.GetBinContent(ibin): # truncate if necessary
               syst = CV - hStatDown.GetBinContent(ibin)
           hSystDown.SetBinContent(ibin, syst)
##           print ('Bin %d: %f + %f + %f - %f - %f' % (ibin, CV, hStatUp.GetBinContent(ibin), hSystUp.GetBinContent(ibin), hStatDown.GetBinContent(ibin), hSystDown.GetBinContent(ibin)))

   
   bg_est = BGEst(hCV, hStatUp, hStatDown, hSystUp, hSystDown, 2001)             
           
   fin.close()

   outfile.cd()
   hCV.Write()
   hStatUp.Write()
   hStatDown.Write()
   hSystUp.Write()
   hSystDown.Write()
   bg_est.gStat.Write()
   bg_est.gSyst.Write()
   bg_est.gFull.Write()

   # and now for aggregate bin predicitons
   for name, asrs in asr_sets.items():
       dASR = outfile.mkdir(name)
       dASR.cd()
       hCV_ASR = Uncertainty(hCV, "all").AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist # pretending the CV is a fully-correlated uncertainty b/c we need to add it linearly
       # stats -- fully uncorrelated
       hStatUp_ASR = Uncertainty(hStatUp).AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
       hStatDown_ASR = Uncertainty(hStatDown).AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
       hCV_ASR.Write()
       
       SYSTSUp_ASR = []
       SYSTSDown_ASR = []
       for hsyst in SYSTS:
           is_correlated = 'all' # the ways these are set up, safe to treat all systs as fully correlated or uncorrelated
           hname = hsyst.GetName()
           if hname.find('MCC') >= 0 or hname.find('NonQCDErr') >= 0:
               is_correlated = ''
           hist_asr = Uncertainty(hsyst, is_correlated).AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
           SYSTSUp_ASR.append(hist_asr)
           SYSTSDown_ASR.append(hist_asr)
       hSystUp_ASR = AddHistsInQuadrature('hSystUp', SYSTSUp_ASR)       
       hSystDown_ASR = AddHistsInQuadrature('hSystDown', SYSTSDown_ASR)
       # sanity: make sure Stat and Syst Down not larger than CV
       for iasr in range(hCV_ASR.GetNbinsX()):
           CV_asr = hCV_ASR.GetBinContent(iasr+1)
           stat_down_asr = hStatDown_ASR.GetBinContent(iasr+1)
           syst_down_asr = hSystDown_ASR.GetBinContent(iasr+1)
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
    fill_qcd_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
   
