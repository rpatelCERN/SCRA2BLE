#!/usr/bin/python
## take data-driven lost lepton estimation from Simon's file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math, TProfile, gDirectory
from uncertainty import Uncertainty
from agg_bins import *

alpha = 1 - 0.6827

def fill_lostlep_hists(inputfile = 'inputs/bg_hists/LLPrediction_Jul26_newSF.root', outputfile = 'inputs/bg_hists/lostlep_hists.root', nbins = 160):
   
   print ('Input file is %s' % inputfile)
   print ('Output file is %s' % outputfile)
   print ('Total number of bins is %d' % nbins)

   TH1D.SetDefaultSumw2(True)
   
   infile = TFile.Open(inputfile);
   hin = infile.Get("Prediction_data/totalPred_LL");
   hsystup = infile.Get("AdditionalContent/totalPropSysUp_LL");
   hsystdown = infile.Get("AdditionalContent/totalPropSysDown_LL");
   hnonclosureup = infile.Get("Prediction_data/totalPredNonClosureUp_LL");
   hnonclosuredown = infile.Get("Prediction_data/totalPredNonClosureDown_LL");
   hAvgWeight = infile.Get("Prediction_MC/avgWeight_LL_MC");

   # load individual systematics
   SYSTS = []
   # shenanigans for ll-tau combination :O
   ## dilep_systs_up = []
   ## dilep_systs_down = []
   ## mu_reco_iso_stats_up = []
   ## mu_reco_iso_stats_down = []
   for h in infile.Get('Prediction_data').GetListOfKeys():
       h = h.ReadObj()
       # skip the histograms that don't actually contain systematics -- make sure you check the names haven't changed
       if h.GetName() == "totalPred_LL" or h.GetName() == "avgWeight_LL" or h.GetName().find('CS') >= 0:
           continue
       ## # convert to absolute
       ## hout = h.Clone()
       ## hout.Reset() 
       for ibin in range(nbins):
           if float(hin.GetBinContent(ibin+1)) == 0.:
               h.SetBinContent(ibin+1, 0.)
           elif h.GetName().find('Up') >= 0:
               h.SetBinContent(ibin+1, (h.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1))
           else:
               h.SetBinContent(ibin+1, (1.-h.GetBinContent(ibin+1))*hin.GetBinContent(ibin+1))           
       SYSTS.append(h)
       ## if h.GetName().find('DiLep') >= 0:
       ##     if h.GetName.find('Up') >= 0:
       ##         dilep_systs_up.append(h)
       ##     else:
       ##         dilep_systs_down.append(h)        
       ## if h.GetName().find('DiLep') >= 0:

           
   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stata and syst uncertainties in these histograms
   hCV = TH1D("hCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatUp = TH1D("hStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatDown = TH1D("hStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystUp = TH1D("hSystUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystDown = TH1D("hSystDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   ## these are the systematics not correlated between lost lepton and tau
   hSystUp_NoTau = TH1D("hSystUp_NoTau", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystDown_NoTau = TH1D("hSystDown_NoTau", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   
   # open text file, extract values
   if nbins != hin.GetNbinsX():
       print ('Warning: input file has %d bins, but I need to fill %d bins!' % (hin.GetNbinsX(), nbins))
   for ibin in range(nbins):
       CV = hin.GetBinContent(ibin+1)
       hCV.SetBinContent(ibin+1, CV)
       hCV.SetBinError(ibin+1, 0.)
       # get stat uncertainties
       stat_up = pow(hAvgWeight.GetBinContent(ibin+1)*1.84102, 2.);
       stat_up += pow(hin.GetBinError(ibin+1), 2.);
       hStatUp.SetBinContent(ibin+1, math.sqrt(stat_up))
       hStatDown.SetBinContent(ibin+1, hin.GetBinError(ibin+1))
       # get syst uncertainties
       syst_up = 0.
       syst_down = 0.
       if hsystup.GetBinContent(ibin+1) > 0.:
           syst_up = syst_up + pow((hsystup.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1), 2.)
       if hsystdown.GetBinContent(ibin+1) > 0.:
           syst_down = syst_down + pow((1.-hsystdown.GetBinContent(ibin+1))*hin.GetBinContent(ibin+1), 2.)
       syst_up = syst_up + pow((hnonclosureup.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1), 2.)
       syst_down = syst_down + pow((1.-hnonclosuredown.GetBinContent(ibin+1))*hin.GetBinContent(ibin+1), 2.)
       syst_up = math.sqrt(syst_up)
       syst_down = math.sqrt(syst_down)
       if syst_down > CV - hStatDown.GetBinContent(ibin+1): # truncate if necessary
           syst_down = CV - hStatDown.GetBinContent(ibin+1)
       hSystUp.SetBinContent(ibin+1, syst_up)
       hSystDown.SetBinContent(ibin+1, syst_down)

             
   outfile.cd()
   hCV.Write()
   hStatUp.Write()
   hStatDown.Write()
   hSystUp.Write()
   hSystDown.Write()

   dTau = outfile.mkdir('corr_tau')
   dTau.cd()
   ## now save the systematics correlated with tau in a subdirectory
   for hsyst in SYSTS:
       hname = hsyst.GetName()
       if hname.find('MuIso') >= 0 or hname.find('MuReco') >= 0 or hname.find('MuAcc') >= 0 or hname.find('DiLep') >= 0:
          hsyst.Write()

   outfile.cd()
   # and now for aggregate bin predicitons
   for name, asrs in asr_sets.items():
       dASR = outfile.mkdir("/".join([name, 'corr_tau']))
       dASR.cd()
       hCV_ASR = Uncertainty(hCV, "all").AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist # pretending the CV is a fully-correlated uncertainty b/c we need to add it linearly
       # stat uncertainty fully-uncorrelated (160 CRs)
       hStatUp_ASR = Uncertainty(hStatUp, '').AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist 
       hStatDown_ASR = Uncertainty(hStatDown, '').AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
       hCV_ASR.Write()
       
       SYSTSUp_ASR = []
       SYSTSDown_ASR = []
       for hsyst in SYSTS:
           hname = hsyst.GetName()
           correlation = 'htmht:nbjets' # note:default is correlated across these dimensions, corresponds to mTEff, SLpurity, DL
           if hname.find('NonClosure') >= 0: # one for each bin
               correlation = ''
           elif hname.find('IsoTrack') >= 0: # only binned in HT and MHT
               correlation = 'njets:nbjets'
           elif hname.find('Iso') >= 0 or hname.find('Reco') >= 0: # binned in properties of lepton, fully-correlated across search bins
               correlation = 'all'
           elif hname.find('Acc') >= 0: # funny
               correlation = 'LLAcc'
           ## store the systeamtics correlated between lost lepton and tau in a subdirectory
           hist_asr = Uncertainty(hsyst, correlation).AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
           # note: the code below successfully write the histograms to each corr_tau subdirectory, but also give the error
           # Error in <TDirectoryFile::cd>: Unknown directory corr_tau -- WHY?
           if hname.find('MuIso') >= 0 or hname.find('MuReco') >= 0 or hname.find('MuAcc') >= 0 or hname.find('DiLep') >= 0:
               dASR.cd("corr_tau")
               hist_asr.Write()                
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
    fill_lostlep_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
   
