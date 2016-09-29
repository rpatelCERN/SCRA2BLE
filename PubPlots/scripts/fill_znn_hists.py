## take data-driven Z-->inv estimation from Bill's file, fill histograms and store them in a root file

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math

alpha = 1 - 0.6827

def main(argv):
   inputfile = 'inputs/bg_hists/ZinvHistos.root'
   outputfile = 'inputs/bg_hists/znn_hists.root'
   nbins = 160
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('fill_znn_hists.py -i <inputfile> -o <outputfile> -n <nbins>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('fill_znn_hists.py -i <inputfile> -o <outputfile> -n <nbins>')
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
   hin = infile.Get("ZinvBGpred");
   hin_systup = infile.Get("ZinvBGsysUp");
   hin_0evt_statup = infile.Get("ZinvBG0EVsysUp");
   hin_systdown = infile.Get("ZinvBGsysLow");

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
       print 'Warning: input file has %d bins, but I need to fill %d bins!' % (hin.GetNbinsX(), nbins)
   for ibin in range(nbins):
       CV = hin.GetBinContent(ibin+1)
       hFullCV.SetBinContent(ibin+1, CV)
       hFullCV.SetBinError(ibin+1, 0.)
       # get stat uncertainties
       stat_up = hin.GetBinError(ibin+1);
       if stat_up==0.:
           stat_up = hin_0evt_statup.GetBinError(ibin+1)
       hFullStatUp.SetBinContent(ibin+1, stat_up)
       stat_down = hin.GetBinError(ibin+1)
       if stat_down > CV: # for some reason, this one is sometimes greater than the central value, so truncate
           stat_down = CV
       hFullStatDown.SetBinContent(ibin+1, stat_down)
       # get syst uncertainties
       syst_up = hin_systup.GetBinContent(ibin+1)
       syst_down = hin_systdown.GetBinContent(ibin+1)
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
   
