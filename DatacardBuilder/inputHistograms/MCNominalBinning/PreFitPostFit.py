import ROOT as root
from ROOT import *
import ROOT
import time
from array import array
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import math
import tdrstyle
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPadLeftMargin(0.12);
ROOT.gStyle.SetPadRightMargin(0.08);
ROOT.gStyle.SetPadTopMargin(0.08);
ROOT.gStyle.SetPalette(1);


#########################################################################################################
def GetPrefitErrorsFromJack(fn):
	f = open(fn,'r');

	errup = [];
	errdn = [];
	for line in f:
		linelist = line.strip().split();
		#print linelist;
		errup.append(float(linelist[1]))
		errdn.append(float(linelist[2]))
		#print errup, errdn
		#errup.append( math.sqrt( float(linelist[4])*float(linelist[4]) + float(linelist[6])*float(linelist[6]) ) );
		#errdn.append( math.sqrt( float(linelist[8])*float(linelist[8]) + float(linelist[10])*float(linelist[10]) ) );

	return (errup,errdn);

def getErrorFromCard(card,chan):

	lnNSystematics = [];

	fcard=open(card)
	column = -1;
	sysLine = False;
	for line in fcard:
		parse=line.split(' ')
		if parse[0]=='process' and parse[1]=='sig':
			for i in range(len(parse)):
				if parse[i] == chan: 
					column = i;

		if parse[0]=='lumi': sysLine = True; #it's time to collect
		if sysLine and parse[1] == "lnN": 
			parse = [x for x in parse if x != '']				
			print "blah,",parse[0],parse[column+1],column,parse				
			if parse[column+1] != "-": 
				if '/' in parse[column+1]: 
					syssplit = parse[column+1].split('/');
					lnNSystematics.append(float(syssplit[1])-1.0);
				else:
					lnNSystematics.append(float(parse[column+1])-1.0);

	print lnNSystematics
	return 0.5

if __name__ == '__main__':
	
	#theDir = 'testCards-allBkgs-SMSbbbb1500-2.1-mu0.0'
	# theDir = 'testCards-allBkgswithPho-SMSbbbb1500-2.1-mu0.0'
	#theDir = 'testCards-allBkgsTestingFit-SMSbbbb1500-2.1-mu0.0';
	fin=TFile("ZinvHistos.root", "READ")
	#fin=TFile("/fdata/hepx/store/user/rish/CombineCards//CMSSW_7_4_7/src/SCRA2BLE/DatacardBuilder/"+"/mlfittestCards-allBkgs-T1tttt_1200_800-24.5-mu0.0.root", "READ")
	BinProcesses=fin.Get("ZinvBGpred");

	YieldsFile=TFile("BkgInputCards.root", "READ")
	histZ=YieldsFile.Get("ZInvBkgSR")
	#Gymnastics for Pre-fit

	znn_penn_red = TColor(2002, 255/255.,0/255.,43/255.);
	
	histZ.SetLineColor(kBlack);

	# hsprefit_tot.SetFillStyle(3004);
	# hsprefit_tot.SetFillColor(1);

	canPostAN = TCanvas("canPostAN","canPre",1600,800);
	p1AN = TPad("p1","p1",0.0,0.3,1.0,0.97)
	p1AN.SetBottomMargin(0.05)
	p1AN.SetNumber(1)
	p2AN = TPad("p2","p2",0.0,0.00,1.0,0.3)
	p2AN.SetNumber(2)
	p2AN.SetTopMargin(0.05)
	p2AN.SetBottomMargin(0.30)	
	canPostAN.cd()
	p1AN.Draw(); p1AN.cd();
	histZ.SetFillColor(0)
	histZ.SetLineColor(kBlack);
	histZ.Draw('pe');
	#BinProcesses.SetLineWidth(1.0)
	BinProcesses.SetLineColor(2002);
	BinProcesses.SetFillColor(2002);
	
	BinProcesses.Draw("pesame");
	histZ.SetTitle('; bin; yield')
	gPad.SetLogy();
	canPostAN.SaveAs("prestack.pdf");
	BinProcesses.SetFillColor(2002);
	Ratio=BinProcesses.Clone("Ratio")	
	#Ratio.Divide(histZ);
	canPostAN.cd()
	p2AN.Draw()
	p2AN.cd()
	
	#rp = TRatioPlot(Ratio, hist);
	#rp.Draw()
	#Ratio.Draw("pe")
