#!/usr/bin/python
## take data-driven hadronic tau estimation from Aditee's file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math, TKey, gDirectory
from uncertainty import Uncertainty
from agg_bins import *

alpha = 1 - 0.6827

def fill_hadtau_hists(inputfile = 'inputs/bg_hists/ARElog60_12.9ifb_HadTauEstimation_data_formatted_New.root', outputfile = 'hadtau_hists.root', nbins = 160):
   
   print ('Input file is %s' % inputfile)
   print ('Output file is %s' % outputfile)
   print ('Total number of bins is %d' % nbins)

   TH1D.SetDefaultSumw2(True)
   
   infile = TFile.Open(inputfile)
   hin = infile.Get("searchBin_nominal_fullstatuncertainty")
   hin_stats = infile.Get("searchBin_StatUncertainties")

   # load many syst hists ...
   symsysts = []
   upsysts = []
   downsysts = []
   for key in infile.GetListOfKeys():
        kname = key.GetName()
        if "QCDBin_" in kname or "nominal" in kname or "searchBin_Stat" in kname or "BMistag" in kname:
            continue
        hist = infile.Get(kname)
        ## if "" in kname or "" in kname:
        ##     specialsysts.append(hist)
        ##     # print 'Special systematic: ' + hist.GetName()
        if ("Dn" in kname or kname == 'searchBin_MTSysUp') and kname != 'searchBin_MTSysDn':
            for ibin in range(hist.GetNbinsX()):
                CV = hin.GetBinContent(ibin+1) 
                hist.SetBinContent(ibin+1, (hist.GetBinContent(ibin+1)-1.)*CV)
            upsysts.append(hist) # yes, this is counterintuitive, just go with it
            #print ('Up systematic: ' + hist.GetName())
        elif ("Up" in kname or kname == 'searchBin_MTSysDn') and kname != 'searchBin_MTSysUp':
            for ibin in range(hist.GetNbinsX()):
                CV = hin.GetBinContent(ibin+1) 
                hist.SetBinContent(ibin+1, (1.-hist.GetBinContent(ibin+1))*CV)
            downsysts.append(hist)
        else:
            for ibin in range(hist.GetNbinsX()):
                CV = hin.GetBinContent(ibin+1) 
                hist.SetBinContent(ibin+1, (hist.GetBinContent(ibin+1)-1.)*CV)
            symsysts.append(hist)
            #print ('Symmetric systematic: ' + hist.GetName())

   ## treat bonkers BMistag systematics separately
   bmistags_in = [infile.Get("searchBin_BMistagUp"), infile.Get("searchBin_BMistagDn")]
   specialsysts = [TH1D("jack_BMistagUp", "", nbins, 0.5, nbins + 0.5), TH1D("jack_BMistagDn", "", nbins, 0.5, nbins + 0.5)]
   for hbmistag_in in bmistags_in:
       for ibin in range(hist.GetNbinsX()):
           CV = hin.GetBinContent(ibin+1)
           if hbmistag_in.GetBinContent(ibin+1) > 1.: # these can migrate in either direction -- put all > 1 in Up and all < 1 in Dn
               specialsysts[0].SetBinContent(ibin+1, (hbmistag_in.GetBinContent(ibin+1)-1.)*CV)
           else:
               specialsysts[1].SetBinContent(ibin+1, (1.-hbmistag_in.GetBinContent(ibin+1))*CV)

   # a tiny bit of re-ordering to make it easier to combine ll and tau correlations                 
   SYSTS = symsysts + downsysts + upsysts + specialsysts
   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stat and syst uncertainties in these histograms
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
       stat_up = hin.GetBinError(ibin+1)
       stat_down = hin_stats.GetBinContent(ibin+1)
       hStatUp.SetBinContent(ibin+1, stat_up)
       hStatDown.SetBinContent(ibin+1, stat_down)
       # get syst uncertainties
       syst_up = 0.
       syst_down = 0.
       for hsyst in symsysts:
           ## hsyst.Write()
           ## syst_up = syst_up + pow((hsyst.GetBinContent(ibin+1)-1.)*CV, 2.)
           ## syst_down = syst_down + pow((hsyst.GetBinContent(ibin+1)-1.)*CV, 2.)
           syst_up = syst_up + hsyst.GetBinContent(ibin+1)**2
           syst_down = syst_down + hsyst.GetBinContent(ibin+1)**2
       for hsyst in upsysts:
           syst_up = syst_up + hsyst.GetBinContent(ibin+1)**2
       for hsyst in downsysts:
           syst_down = syst_down + hsyst.GetBinContent(ibin+1)**2
       ## BMistags
       syst_up = syst_up + specialsysts[0].GetBinContent(ibin+1)**2
       syst_down = syst_down + specialsysts[1].GetBinContent(ibin+1)**2
       syst_up=math.sqrt(syst_up)
       syst_down=math.sqrt(syst_down)            
       if syst_down > CV - hStatDown.GetBinContent(ibin+1): # truncate if necessary
           syst_down = CV - hStatDown.GetBinContent(ibin+1)
       hSystUp.SetBinContent(ibin+1, syst_up)
       hSystDown.SetBinContent(ibin+1, syst_down)
       
       # print ('Bin %d: %f + %f + %f - %f - %f' % (ibin+1, CV, hStatUp.GetBinContent(ibin+1), hSystUp.GetBinContent(ibin+1), hStatDown.GetBinContent(ibin+1), hSystDown.GetBinContent(ibin+1)))
           
             
   outfile.cd()
   hCV.Write()
   hStatUp.Write()
   hStatDown.Write()
   hSystUp.Write()
   hSystDown.Write()

   dLL = outfile.mkdir('corr_ll')
   dLL.cd()
   ## now save the systematics correlated with lost lepton in a subdirectory
   for hsyst in SYSTS:
       hname = hsyst.GetName()
       if hname.find('MuIso') >= 0 or hname.find('MuReco') >= 0 or hname.find('MuAcc') >= 0 or hname.find('Dilep') >= 0:
           hsyst.Write()
   
   outfile.cd()
   # and now for aggregate bin predicitons
   for name, asrs in asr_sets.items():
       dASR = outfile.mkdir("/".join([name, 'corr_ll']))
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
           correlation = 'all' # note: default is fully-correlated across all bins, corresponds to MuIso, MuReco, MuRecoIso (stat), JECSys, Dilepton, MTSys
           if hname.find('adhoc') >= 0:
               correlation = 'htmht' ## adhoc fudge factor is binned in njets & nbjets
           elif hname.find('closure') >= 0: # one for each bin
               correlation = ''
           elif hname.find('TrigEff') >= 0: # only binned in HT and MHT
               correlation = 'njets:nbjets'
           elif hname.find('Acc') >= 0 or hname.find('IsoTrk') >= 0 or hname.find('MtEff') >= 0 or hname.find('MuFromTau') >= 0 or hname.find('BMistag') >= 0: # not binned in nbjets
               correlation = 'nbjets'
           ## store the systeamtics correlated between lost lepton and tau in a subdirectory
           hist_asr = Uncertainty(hsyst, correlation).AggregateBins(asrs, asr_xtitle[name], asr_xbins[name]).hist
           # note: the code below successfully writes the histograms to each corr_tau subdirectory, but also gives the error
           # Error in <TDirectoryFile::cd>: Unknown directory corr_ll -- WHY?
           if hname.find('MuIso') >= 0 or hname.find('MuReco') >= 0 or hname.find('Acc') >= 0 or hname.find('Dilep') >= 0 or hname.find('BMistag') >= 0:
               dASR.cd("corr_ll")
               hist_asr.Write()                
           ## now group by Up, Down, symmetric
           if hname.find('Dn') >= 0:
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
    fill_hadtau_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
   
