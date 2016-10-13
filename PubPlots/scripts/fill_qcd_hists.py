#!/usr/bin/python
## take data-driven QCD estimation from text file, fill histograms and store them in a root file

from __future__ import print_function

import os
import sys, getopt
import math
from ROOT import TFile, TH1D, Math
from bg_est import BGEst

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
               for isyst in range(8, len(values)-7):
                   syst = syst + pow((float(values[isyst])-1.)*CV, 2.)
               syst = math.sqrt(syst)
           hSystUp.SetBinContent(ibin, syst)
           if syst > CV - hStatDown.GetBinContent(ibin): # truncate if necessary
               syst = CV - hStatDown.GetBinContent(ibin)
           hSystDown.SetBinContent(ibin, syst)
           print ('Bin %d: %f + %f + %f - %f - %f' % (ibin, CV, hStatUp.GetBinContent(ibin), hSystUp.GetBinContent(ibin), hStatDown.GetBinContent(ibin), hSystDown.GetBinContent(ibin)))

   
   bg_est = BGEst(hCV, hStatUp, hStatDown, hSystUp, hSystDown)             
           
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
   outfile.Close()
        
if __name__ == "__main__":
    import sys
    fill_qcd_hists(sys.argv[1], sys.argv[2], int(sys.argv[3]))
   
