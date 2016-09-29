## take data-driven lost lepton estimation from Simon's file, fill histograms and store them in a root file

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math, TProfile

alpha = 1 - 0.6827

def main(argv):
   inputfile = 'inputs/bg_hists/LLPrediction_Jul26_newSF.root'
   outputfile = 'inputs/bg_hists/lostlep_hists.root'
   nbins = 160
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('fill_lostlep_hists.py -i <inputfile> -o <outputfile> -n <nbins>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('fill_lostlep_hists.py -i <inputfile> -o <outputfile> -n <nbins>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-n", "--nbins"):
         nbins = arg
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

   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stata and syst uncertainties in these histograms
   hFullCV = TH1D("hFullCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullStatUp = TH1D("hFullStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullStatDown = TH1D("hFullStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullSystUp = TH1D("hFullSystUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullSystDown = TH1D("hFullSystDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   
   # open text file, extract values
   if nbins != hin.GetNbinsX():
       print 'Warning: input file has %d bins, but I need to fill %d bins!' % (hin.GetNbinsX(), nbins)
   for ibin in range(nbins):
       CV = hin.GetBinContent(ibin+1)
       hFullCV.SetBinContent(ibin+1, CV)
       hFullCV.SetBinError(ibin+1, 0.)
       # get stat uncertainties
       stat_up = pow(hAvgWeight.GetBinContent(ibin+1)*1.84102, 2.);
       stat_up += pow(hin.GetBinError(ibin+1), 2.);
       hFullStatUp.SetBinContent(ibin+1, math.sqrt(stat_up))
       hFullStatDown.SetBinContent(ibin+1, hin.GetBinError(ibin+1))
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
       if syst_down > CV - hFullStatDown.GetBinContent(ibin+1): # truncate if necessary
           syst_down = CV - hFullStatDown.GetBinContent(ibin+1)
       hFullSystUp.SetBinContent(ibin+1, syst_up)
       hFullSystDown.SetBinContent(ibin+1, syst_down)
       print 'Bin %d: %f + %f + %f - %f - %f' % (ibin+1, CV, hFullStatUp.GetBinContent(ibin+1), hFullSystUp.GetBinContent(ibin+1), hFullStatDown.GetBinContent(ibin+1), hFullSystDown.GetBinContent(ibin+1))
           
             
   outfile.cd()
   hFullCV.Write()
   hFullStatUp.Write()
   hFullStatDown.Write()
   hFullSystUp.Write()
   hFullSystDown.Write()
   outfile.Close()
        
if __name__ == "__main__":
   main(sys.argv[1:])
   
