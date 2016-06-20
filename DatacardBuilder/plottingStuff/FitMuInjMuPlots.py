import os
import glob
import math
import array
import sys
import time
import ROOT
from array import array
import numpy as np
import tdrstyle
tdrstyle.setTDRStyle()

def ExtractFile(iname):
	f = ROOT.TFile(iname);
	t = f.Get("limit");
	fitmu=[]
	t.GetEntry(0);
	fitmu.append(t.limit)
	t.GetEntry(1);
	fitmu.append(t.limit)
	t.GetEntry(2);
	fitmu.append(t.limit)

	return fitmu;

if __name__ == '__main__':
	idir = "../";
	models=["SMSbbbb1000"]
	#injMu=[0.0,2.0,3.0,4.0,5.0]
	injMu=[0.0,2.0,3.0,4.0, 5.0]
	can = ROOT.TCanvas("can","can",1200,800);
	hrl = ROOT.TH2F("hrl","hrl",6,0,6,6,0,6);
	hrl.GetYaxis().SetTitle("#mu_{fit}");
	hrl.GetXaxis().SetTitle("#mu_{inj}");
	hrl.Draw()
	a_injMu = np.asarray(injMu)
	for m in models:
		fitMus=[]
		for mu in injMu:
			#print idir+"higgsCombinetestCards-allBkgs-%s-3.0-mu%1.1f.MaxLikelihoodFit.mH120.root" %(m,mu)
			fitMus.append(ExtractFile(idir+"higgsCombinetestCards-allBkgs-%s-3.0-mu%1.1f.MaxLikelihoodFit.mH120.root" %(m,mu))[0])
		a_fitMus=np.asarray(fitMus)
		g_mufit = ROOT.TGraph(len(injMu), a_injMu, a_fitMus)
		print fitMus
		g_mufit.Draw("LPSame")
	can.Print("MuInjTest.pdf")
