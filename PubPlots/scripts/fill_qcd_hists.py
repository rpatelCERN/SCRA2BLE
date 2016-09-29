## take data-driven QCD estimation from text file, fill histograms and store them in a root file

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math

alpha = 1 - 0.6827

def main(argv):
   inputfile = 'inputs/bg_hists/qcd-bg-combine-input-12.9ifb-july28-nodashes.txt'
   outputfile = 'inputs/bg_hists/qcd_hists.root'
   nbins = 160
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('fill_qcd_hists.py -i <inputfile> -o <outputfile> -n <nbins>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('fill_qcd_hists.py -i <inputfile> -o <outputfile> -n <nbins>')
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
   outfile = TFile(outputfile, "recreate")
   outfile.cd()

   # store the central values, +/1 stata and syst uncertainties in these histograms
   hFullCV = TH1D("hFullCV", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullStatUp = TH1D("hFullStatUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullStatDown = TH1D("hFullStatDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullSystUp = TH1D("hFullSystUp", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   hFullSystDown = TH1D("hFullSystDown", ";Search Bin;Events / Bin", nbins, 0.5, nbins + 0.5)
   
   # open text file, extract values
   with open(inputfile) as fin:
       num_lines = sum(1 for line in fin)
       ibin = -1
       if nbins+1 != num_lines:
           print 'Warning: text file has %d lines, but I need to fill %d bins!' % (num_lines, nbins)
       fin.seek(0)
       for line in fin:
           ibin = ibin+1
           if ibin < 1:
               continue
           values = line.split()
           if len(values) != 32:
               print 'Warning: this line looks funny'
           CV = abs(max(float(values[len(values)-3]), 0.))
           hFullCV.SetBinContent(ibin, CV)
           hFullCV.SetBinError(ibin, 0.)
           # get stat uncertainties from CR observation - EWK contamination
           NLDP = float(values[2])
           RQCD = float(values[6])
           N_nonQCD = float(values[3])
           NCR = max(NLDP-N_nonQCD, 0.)
           L = 0.
           if NCR > 0.:
               L = Math.gamma_quantile(alpha/2,NCR,1.)
           U = Math.gamma_quantile_c(alpha/2,NCR+1,1.)
           hFullStatUp.SetBinContent(ibin,RQCD*(U-NCR))
           hFullStatDown.SetBinContent(ibin,RQCD*(NCR-L))
           err_nonQCD = max(RQCD*float(values[5]), 0.)
           syst = 0.
           if CV > 0.:
               syst = syst + pow(err_nonQCD, 2.)
               for isyst in range(8, len(values)-7):
                   syst = syst + pow((float(values[isyst])-1.)*CV, 2.)
               syst = math.sqrt(syst)
           hFullSystUp.SetBinContent(ibin, syst)
           if syst > CV - hFullStatDown.GetBinContent(ibin): # truncate if necessary
               syst = CV - hFullStatDown.GetBinContent(ibin)
           hFullSystDown.SetBinContent(ibin, syst)
           print 'Bin %d: %f + %f + %f - %f - %f' % (ibin, CV, hFullStatUp.GetBinContent(ibin), hFullSystUp.GetBinContent(ibin), hFullStatDown.GetBinContent(ibin), hFullSystDown.GetBinContent(ibin))
           
  
           
   fin.close()

   outfile.cd()
   hFullCV.Write()
   hFullStatUp.Write()
   hFullStatDown.Write()
   hFullSystUp.Write()
   hFullSystDown.Write()
   outfile.Close()
        
if __name__ == "__main__":
   main(sys.argv[1:])
   
