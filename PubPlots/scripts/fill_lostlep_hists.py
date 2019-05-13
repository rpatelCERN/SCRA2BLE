#!/usr/bin/python
## take data-driven lost lepton estimation from Simon's file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
from math import sqrt
from ROOT import TFile, TH1D, Math, TProfile, gDirectory
from uncertainty import Uncertainty
from agg_bins import *

alpha = 1 - 0.6827

def fill_lostlep_hists(inputfile = 'inputs/bg_hists/LLPrediction.root', outputfile = 'lostlep_hists.root', nbins = 174, lumiSF=1.):
   
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
   hAvgWeight = infile.Get("Prediction_data/avgWeight_0L1L");

   # load individual systematics
   SYSTS = []
   for h in infile.Get('Prediction_data').GetListOfKeys():
       h = h.ReadObj()
       # skip the histograms that don't actually contain systematics -- make sure you check the names haven't changed
       if h.GetName() == "totalPred_LL" or h.GetName() == "avgWeight_0L1L" or h.GetName()=="totalPredControlStat_LL" or h.GetName().find('CS') >= 0:
           continue
       # convert to absolute
       hout = h.Clone()
       hout.Reset() 
       for ibin in range(nbins):
           if float(hin.GetBinContent(ibin+1)) == 0.:
               hout.SetBinContent(ibin+1, 0.)
           elif h.GetName().find('Up') >= 0:
               hout.SetBinContent(ibin+1, lumiSF*(h.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1))
           else:
               hout.SetBinContent(ibin+1, lumiSF*(1.-h.GetBinContent(ibin+1))*hin.GetBinContent(ibin+1))           
       SYSTS.append(hout)

           
   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stata and syst uncertainties in these histograms
   hCV = TH1D("hCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatUp = TH1D("hStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatDown = TH1D("hStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystUp = TH1D("hSystUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystDown = TH1D("hSystDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   
   if nbins != hin.GetNbinsX():
       print ('Warning: input file has %d bins, but I need to fill %d bins!' % (hin.GetNbinsX(), nbins))
   for ibin in range(nbins):
       CV = lumiSF*hin.GetBinContent(ibin+1)
       hCV.SetBinContent(ibin+1, CV)
       hCV.SetBinError(ibin+1, 0.)
       # get stat uncertainties
       stat_up = pow(hAvgWeight.GetBinContent(ibin+1)*1.84102, 2.);
       stat_up += pow(lumiSF*hin.GetBinError(ibin+1), 2.);
       stat_up = sqrt(stat_up)
       hStatUp.SetBinContent(ibin+1, stat_up)
       stat_down = lumiSF*hin.GetBinError(ibin+1)
       if stat_down > CV: # just to be safe
               stat_down = CV
       hStatDown.SetBinContent(ibin+1, stat_down)
       # get syst uncertainties
       syst_up = 0.
       syst_down = 0.
       for hsyst in SYSTS:
           if hCV.GetBinContent(ibin+1) > 0.:
               syst_up = syst_up + hsyst.GetBinContent(ibin+1)**2
               syst_down = syst_down + hsyst.GetBinContent(ibin+1)**2
       syst_up = sqrt(syst_up) #should be already scaled
       syst_down = sqrt(syst_down)
       ## syst_up = syst_up + pow((hnonclosureup.GetBinContent(ibin+1)-1.)*CV, 2.)
       ## syst_down = syst_down + pow((1.-hnonclosuredown.GetBinContent(ibin+1))*CV, 2.)
       ## syst_up = lumiSF*sqrt(syst_up) # these need to be scaled because they're not coming from the individual systs that we already scaled
       ## syst_down = lumiSF*sqrt(syst_down)
       if syst_down > sqrt(CV**2 - hStatDown.GetBinContent(ibin+1)**2): # truncate if necessary
           syst_down = sqrt(CV**2 - hStatDown.GetBinContent(ibin+1)**2)
       hSystUp.SetBinContent(ibin+1, syst_up)
       hSystDown.SetBinContent(ibin+1, syst_down)
       print ("Bin %d: %3.2f + %3.2f + %3.2f - %3.2f - %3.2f" % (ibin+1, CV, stat_up, syst_up, stat_down, syst_down))

             
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
           correlation = 'htmht:nbjets' # note:default is correlated across these dimensions, corresponds to mTEff, SLpurity, DL
           if hname.find('NonClosure') >= 0 or hname.find('IsoTrackStat') >= 0 or hname.find('MTWStat') >= 0 or hname.find('AccStat') >= 0: # one for each bin
               correlation = ''
           elif hname.find('Iso') >= 0 or hname.find('Reco') >= 0: # binned in properties of lepton, fully-correlated across search bins -- now includes isolated track sys
               correlation = 'all'
           elif hname.find('MTWSys') >= 0 or hname.find('Acc') >= 0: # binned in htmht, njets
               correlation = 'nbjets'
           ## elif hname.find('Acc') >= 0: # funny
           ##     correlation = 'LLAcc'
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
    fill_lostlep_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
   
