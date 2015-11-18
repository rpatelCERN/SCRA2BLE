import re
import os
import sys
import ROOT
from ROOT import *

import tdrstyle
tdrstyle.setTDRStyle()
gStyle.SetPadLeftMargin(0.12);
gStyle.SetPadRightMargin(0.08);
gStyle.SetPadTopMargin(0.08);
gStyle.SetPalette(1);

import time
f=open("%s.txt" %sys.argv[1],'r')

Nuisance=TH1F("Nuisance", "#Delta X / #sigma_{pre}", 366, 0,366)
NuisanceSigma=TH1F("NuisanceSigma", "#sigma_{fit} / #sigma_{pre}", 366, 0,366)

ZNuisLines=[]
QCDNuisLines=[]
SLHadTauNuisLine=[]
HadTauNuisLines=[]
SignalNuis=[]
bin=1

for line in f:
	linep = line.replace(',',' , ');
	parse = linep.split();
	# parse=re.split(' |, |',line);
	#print parse

	goodrow = False;
	for i in range(len(parse)):
			
		if parse[i]=='':continue
		if parse[0].find("LLSC")>-1 or parse[0].find("ldp")>-1 or parse[0].find("contam")>-1 or parse[0].find("SPho")>-1 or parse[0].find("name")>-1: break;	
		else:
			goodrow = True;
			# print linep
			# print parse
			# if column==1 :
			# 	#Nuisance.SetBinContent(bin,float(parse[i]))
						
			# 	if parse[0].find("KQCD")>-1:NuisanceQCD.SetBinContent(bin, float(parse[i]))
			# 	if parse[0].find("LL")>-1 or parse[0].find("MuAcc")>-1 or  parse[0].find("ElecAcc")>-1:NuisanceSL.SetBinContent(bin, float(parse[i]))		
			# 	if parse[0].find("DY")>-1 or parse[0].find("Zg")>-1 or parse[0].find("Pho")>-1: 
			# 		NuisanceZ.SetBinContent(bin, float(parse[i]))
			# 	if parse[0].find("HadTau")>-1: 
			# 		NuisanceHadTau.SetBinContent(bin, float(parse[i]))

			# 	if parse[0].find("KQCD")>-1: QCDNuisLines.append(line)
			# 	if(parse[0].find("DY")>-1 or parse[0].find("Zg")>-1 or parse[0].find("Pho")>-1):ZNuisLines.append(line)
			# 	if(parse[0].find("LL")>-1 or parse[0].find("MuAcc")>-1 or  parse[0].find("ElecAcc")>-1):SLHadTauNuisLine.append(line)
   #                              if(parse[0].find("HadTau")>-1):HadTauNuisLines.append(line)
			if i==1:
				Nuisance.SetBinContent(bin,float(parse[i]))
				# if(float(parse[i]>0.9)):print parse[0]
				SignalNuis.append(parse[0])	
			if i==3:
				NuisanceSigma.SetBinContent(bin,(float(parse[i])))		
  				# if parse[0].find("KQCD")>-1:NuisanceSigmaQCD.SetBinContent(bin, float(parse[i]))
      #                           if parse[0].find("LL")>-1 or parse[0].find("MuAcc") or  parse[0].find("ElecAcc"):NuisanceSigmaSL.SetBinContent(bin, float(parse[i]))
      #                           if parse[0].find("DY")>-1 or parse[0].find("Zg")>-1 or parse[0].find("Pho")>-1: NuisanceSigmaZ.SetBinContent(bin, float(parse[i]))
      #                           if parse[0].find("HadTau")>-1:NuisanceSigmaHadTau.SetBinContent(bin, float(parse[i]))

	if goodrow: bin=bin+1

#time.sleep(60)
# fout.cd()

Nuisance.GetXaxis().SetTitle("Total Nuisances")
Nuisance.GetYaxis().SetTitle("#Delta X / #sigma_{pre}")
# NuisanceQCD.GetXaxis().SetTitle("Total Nuisances")
# NuisanceQCD.GetYaxis().SetTitle("#Delta X / #sigma_{pre}")
# NuisanceSL.GetXaxis().SetTitle("Total Nuisances")
# NuisanceSL.GetYaxis().SetTitle("#Delta X / #sigma_{pre}")
# NuisanceZ.GetXaxis().SetTitle("Total Nuisances")
# NuisanceZ.GetYaxis().SetTitle("#Delta X / #sigma_{pre}")
# NuisanceHadTau.GetXaxis().SetTitle("Total Nuisances")
# NuisanceHadTau.GetYaxis().SetTitle("#Delta X / #sigma_{pre}")


NuisanceSigma.GetXaxis().SetTitle("Total Nuisances")
NuisanceSigma.GetYaxis().SetTitle("#sigma_{fit} / #sigma_{pre}")
# NuisanceSigmaQCD.GetXaxis().SetTitle("Total Nuisances")
# NuisanceSigmaQCD.GetYaxis().SetTitle("#sigma_{fit} / #sigma_{pre}")
# NuisanceSigmaSL.GetXaxis().SetTitle("Total Nuisances")
# NuisanceSigmaSL.GetYaxis().SetTitle("#sigma_{fit} / #sigma_{pre}")
# NuisanceSigmaZ.GetXaxis().SetTitle("Total Nuisances")
# NuisanceSigmaZ.GetYaxis().SetTitle("#sigma_{fit} / #sigma_{pre}")
# NuisanceSigmaHadTau.GetXaxis().SetTitle("Total Nuisances")
# NuisanceSigmaHadTau.GetYaxis().SetTitle("#sigma_{fit} / #sigma_{pre}")

for i in range(bin-1):
	Nuisance.GetXaxis().SetBinLabel(i+1,SignalNuis[i]);
	NuisanceSigma.GetXaxis().SetBinLabel(i+1,SignalNuis[i]);

print "bin = ", bin
canCen = TCanvas("canCen","canCen",1800,800);
Nuisance.GetXaxis().SetRangeUser(0,bin)
Nuisance.Draw();
canCen.SaveAs("nuisances/nuis_"+sys.argv[1]+".pdf")
print "bin2 = ", bin
canSig = TCanvas("canSig","canSig",1800,800);
NuisanceSigma.GetXaxis().SetRangeUser(0,bin)
NuisanceSigma.Draw();
canSig.SaveAs("nuisances/nuis_"+sys.argv[1]+"_sig.pdf")
# Nuisance.Write()
# NuisanceSigma.Write()	

#NuisanceQCD.Write()
#NuisanceSigmaQCD.Write()

#NuisanceSL.Write()
#NuisanceSigmaSL.Write()	

#NuisanceZ.Write()
#NuisanceSigmaZ.Write()

#NuisanceHadTau.Write()
#NuisanceSigmaHadTau.Write()
