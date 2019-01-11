#!/usr/bin/python
## take data-driven hadronic tau estimation from Aditee's file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
from math import sqrt
from ROOT import TFile, TH1D, Math, TKey, gDirectory
from uncertainty import Uncertainty
from agg_bins import *

alpha = 1 - 0.6827

def fill_hadtau_hists(inputfile = 'inputs/bg_hists/ARElog116_35.9ifb_HadTauEstimation_data_formatted_V12.root', outputfile = 'hadtau_hists.root', nbins = 174, lumiSF=1.):

   print ('Input file is %s' % inputfile)
   print ('Output file is %s' % outputfile)
   print ('Total number of bins is %d' % nbins)

   TH1D.SetDefaultSumw2(True)

   infile = TFile.Open(inputfile)
   hin = infile.Get("totalPred_LLPlusHadTau")
   hin_stats_no_poiscl0 = infile.Get("totalPred_LLPlusHadTau")

   # load many syst hists ...
   symsysts = []
   upsysts = []
   downsysts = []
   for key in infile.GetListOfKeys():
        kname = key.GetName()
        if "QCDBin_" in kname or "totalPred_LLPlusHadTau" in kname or "DataCSStatistics" in kname or "LLPlusHadTauTF" in kname or "DataCSStatErr" in kname:
            continue
	if "_Change" in kname or "searchBin_one" in kname or "closureRatio" in kname or "totalPredNonClosure_LL" in kname:continue
        #if "QCDBin_" in kname or "nominal" in kname or "DataCSStatistics" in kname or "BMistag" in kname:
        hist = infile.Get(kname)
        # convert to absolute
        hout = hist.Clone()
        hout.Reset()
        if ('MTSysUp' in kname) and 'MTSysDown' not in kname:
            for ibin in range(hist.GetNbinsX()):
                CV = lumiSF*hin.GetBinContent(ibin+1)
                hout.SetBinContent(ibin+1, (hist.GetBinContent(ibin+1)-1.)*CV)
            upsysts.append(hout) # yes, this is counterintuitive, just go with it
        elif ("Up" in kname) and 'MTSysUp' not in kname:
            for ibin in range(hist.GetNbinsX()):
                CV = lumiSF*hin.GetBinContent(ibin+1)
                hout.SetBinContent(ibin+1, (1.-hist.GetBinContent(ibin+1))*CV)
            downsysts.append(hout)
        else:
            for ibin in range(hist.GetNbinsX()):
                CV = lumiSF*hin.GetBinContent(ibin+1)
                hout.SetBinContent(ibin+1, (hist.GetBinContent(ibin+1)-1.)*CV)
            symsysts.append(hout)
            print ('Symmetric systematic: ' + hist.GetName())
   ## treat bonkers BMistag systematics separately
   # bmistags_in = [infile.Get("totalPredBMistagUp_HadTau"), infile.Get("totalPredBMistagDown_HadTau")]
   # specialsysts = [TH1D("jack_BMistagUp", "", nbins, 0.5, nbins + 0.5), TH1D("jack_BMistagDown", "", nbins, 0.5, nbins + 0.5)]
   # for hbmistag_in in bmistags_in:
   #     for ibin in range(hist.GetNbinsX()):
   #         CV = lumiSF*hin.GetBinContent(ibin+1)
   #         if hbmistag_in.GetBinContent(ibin+1) > 1.: # these can migrate in either direction -- put all > 1 in Up and all < 1 in Down
   #             specialsysts[0].SetBinContent(ibin+1, (hbmistag_in.GetBinContent(ibin+1)-1.)*CV)
   #         else:
   #             specialsysts[1].SetBinContent(ibin+1, (1.-hbmistag_in.GetBinContent(ibin+1))*CV)

   # a tiny bit of re-ordering to make it easier to combine ll and tau correlations -- (if we eventually do this)
   SYSTS = symsysts + downsysts + upsysts
   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stat and syst uncertainties in these histograms
   hCV = TH1D("hCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatUp = TH1D("hStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hStatDown = TH1D("hStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystUp = TH1D("hSystUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hSystDown = TH1D("hSystDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)

   poiscl0 = 0.460255

   if nbins != hin.GetNbinsX():
       print ('Warning: input file has %d bins, but I need to fill %d bins!' % (hin.GetNbinsX(), nbins))
   for ibin in range(nbins):
       CV = lumiSF*hin.GetBinContent(ibin+1)
       hCV.SetBinContent(ibin+1, CV)
       hCV.SetBinError(ibin+1, 0.)
       # get stat uncertainties
       stat = lumiSF*hin_stats_no_poiscl0.GetBinError(ibin+1)
       stat_up = sqrt(stat**2+poiscl0**2)
       stat_down = stat
       if stat_down > CV: # just to be safe
               stat_down = CV
       hStatUp.SetBinContent(ibin+1, stat_up)
       hStatDown.SetBinContent(ibin+1, stat_down)
       # get syst uncertainties
       syst_up = 0.
       syst_down = 0.
       for hsyst in symsysts:
           syst_up = syst_up + hsyst.GetBinContent(ibin+1)**2
           syst_down = syst_down + hsyst.GetBinContent(ibin+1)**2
       for hsyst in upsysts:
           syst_up = syst_up + hsyst.GetBinContent(ibin+1)**2
       for hsyst in downsysts:
           syst_down = syst_down + hsyst.GetBinContent(ibin+1)**2
       ## BMistags
       #syst_up = syst_up + specialsysts[0].GetBinContent(ibin+1)**2
       #syst_down = syst_down + specialsysts[1].GetBinContent(ibin+1)**2
       ## already lumi-scaled
       syst_up = sqrt(syst_up)
       syst_down = sqrt(syst_down)
       if syst_down > sqrt(CV**2 - hStatDown.GetBinContent(ibin+1)**2): # truncate if necessary
           syst_down = sqrt(CV**2 - hStatDown.GetBinContent(ibin+1)**2)
       hSystUp.SetBinContent(ibin+1, syst_up)
       hSystDown.SetBinContent(ibin+1, syst_down)

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
       # stat uncertainty fully-uncorrelated (160 CRs)
       hStatUp_ASR = Uncertainty(hStatUp, '').AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
       hStatDown_ASR = Uncertainty(hStatDown, '').AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
       hCV_ASR.Write()

       SYSTSUp_ASR = []
       SYSTSDown_ASR = []
       for hsyst in SYSTS:
           hname = hsyst.GetName()
           correlation = 'nbjets' # note: default is correlated across nbjets bins, corresponds to Acc, PDF, Scale, IsoTrack, MtEffStat, MuFromTau, BMistag
           if hname.find('Adhoc') >= 0:
               correlation = 'htmht' ## adhoc fudge factor is binned in njets & nbjets
           elif hname.find('NonClosure') >= 0: # one for each bin
               correlation = ''
           elif hname.find('TrigSyst') >= 0: # only binned in HT and MHT
               correlation = 'njets:nbjets'
           elif hname.find('MuReco') >= 0 or hname.find('MuIso') >= 0 or hname.find('MTSys') >= 0 or hname.find('JEC') >= 0 or hname.find('Dilep') >= 0: # 1 value, fully-correlated
               correlation = 'all'
           hist_asr = Uncertainty(hsyst, correlation).AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
           ## now group by Up, Down, symmetric
           #if hname.find('Down') >= 0:
           #    SYSTSDown_ASR.append(hist_asr)
           #elif hname.find('Up') >= 0:
           #    SYSTSUp_ASR.append(hist_asr)
           #else:
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
    fill_hadtau_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
