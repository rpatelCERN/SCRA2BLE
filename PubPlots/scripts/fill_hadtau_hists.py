#!/usr/bin/python
## take data-driven hadronic tau estimation from Aditee's file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math, TKey

alpha = 1 - 0.6827

def fill_hadtau_hists(inputfile = 'inputs/bg_hists/ARElog60_12.9ifb_HadTauEstimation_data_formatted_New.root', outputfile = 'inputs/bg_hists/hadtau_hists.root', nbins = 160):
   
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
   specialsysts = []
   for key in infile.GetListOfKeys():
        kname = key.GetName()
        if "QCDBin_" in kname or "nominal" in kname or "searchBin_Stat" in kname:
            continue
        hist = infile.Get(kname)
        if "BMistag" in kname or "MTSys" in kname:
            specialsysts.append(hist)
            # print 'Special systematic: ' + hist.GetName()
        elif "Dn" in kname:
            upsysts.append(hist) # yes, this is counterintuitive, just go with it
            # print 'Up systematic: ' + hist.GetName()
        elif "Up" in kname:
            downsysts.append(hist)
            # print 'Down systematic: ' + hist.GetName()
        else:
            symsysts.append(hist)
            # print 'Symmetric systematic: ' + hist.GetName()

   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stata and syst uncertainties in these histograms
   hFullCV = TH1D("FullCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullStatUp = TH1D("hFullStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullStatDown = TH1D("hFullStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullSystUp = TH1D("hFullSystUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullSystDown = TH1D("hFullSystDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   
   # open text file, extract values
   if nbins != hin.GetNbinsX():
       print ('Warning: input file has %d bins, but I need to fill %d bins!' % (hin.GetNbinsX(), nbins))
   for ibin in range(nbins):
       CV = hin.GetBinContent(ibin+1)
       hFullCV.SetBinContent(ibin+1, CV)
       hFullCV.SetBinError(ibin+1, 0.)
       # get stat uncertainties
       stat_up = hin.GetBinError(ibin+1)
       stat_down = hin_stats.GetBinContent(ibin+1)
       hFullStatUp.SetBinContent(ibin+1, stat_up)
       hFullStatDown.SetBinContent(ibin+1, stat_down)
       # get syst uncertainties
       syst_up = 0.
       syst_down = 0.
       for hsyst in symsysts:
           syst_up = syst_up + pow((hsyst.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1), 2.)
           syst_down = syst_down + pow((hsyst.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1), 2.)
       for hsyst in upsysts:
           syst_up = syst_up + pow((hsyst.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1), 2.)
       for hsyst in downsysts:
           syst_down = syst_down + pow((1.-hsyst.GetBinContent(ibin+1))*hin.GetBinContent(ibin+1), 2.)
       for hsyst in specialsysts:
           if hsyst.GetBinContent(ibin+1)>1.:
               syst_up = syst_up + pow((hsyst.GetBinContent(ibin+1)-1.)*hin.GetBinContent(ibin+1), 2.)
           else:
               syst_down = syst_down + pow((1.-hsyst.GetBinContent(ibin+1))*hin.GetBinContent(ibin+1), 2.)

       syst_up=math.sqrt(syst_up)
       syst_down=math.sqrt(syst_down)            
       if syst_down > CV - hFullStatDown.GetBinContent(ibin+1): # truncate if necessary
           syst_down = CV - hFullStatDown.GetBinContent(ibin+1)
       hFullSystUp.SetBinContent(ibin+1, syst_up)
       hFullSystDown.SetBinContent(ibin+1, syst_down)
       
       print ('Bin %d: %f + %f + %f - %f - %f' % (ibin+1, CV, hFullStatUp.GetBinContent(ibin+1), hFullSystUp.GetBinContent(ibin+1), hFullStatDown.GetBinContent(ibin+1), hFullSystDown.GetBinContent(ibin+1)))
           
             
   outfile.cd()
   hFullCV.Write()
   hFullStatUp.Write()
   hFullStatDown.Write()
   hFullSystUp.Write()
   hFullSystDown.Write()
   outfile.Close()
        
if __name__ == "__main__":
    import sys
    fill_hadtau_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
   
