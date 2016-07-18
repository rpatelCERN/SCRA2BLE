import ROOT as root
from ROOT import *
import ROOT
import time
import operator
import sys

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import math
import tdrstyle
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPadLeftMargin(0.12);
ROOT.gStyle.SetPadRightMargin(0.08);
ROOT.gStyle.SetPadTopMargin(0.08);
ROOT.gStyle.SetPalette(1);


#########################################################################################################

if __name__ == '__main__':
	model=sys.argv[1]
	mGo=int(sys.argv[2])
	mLSP=int(sys.argv[3])	
	#theDir = 'testCards-allBkgs-SMSbbbb1500-2.1-mu0.0'
	# theDir = 'testCards-allBkgswithPho-SMSbbbb1500-2.1-mu0.0'
	theDir='../testCards-allBkgs-T2tt_%d_%d-7.6-mu0.0/' %(600, 300)
	YieldsFile=TFile(theDir+"/yields.root", "READ")
	histqcd=YieldsFile.Get("QCD")
	histZ=YieldsFile.Get("Zvv")
	histTau=YieldsFile.Get("tau")
	histLL=YieldsFile.Get("LL")
	#Gymnastics for Pre-fit
	DataHist=YieldsFile.Get("data")
	#signalFile=TFile("../inputHistograms/fastsimSignalT2tt/RA2bin_signal.root", "READ")
	#signal=signalFile.Get("RA2bin_T2tt_%d_%d_fast" %(mGo, mLSP))
	signalFile=TFile("../inputHistograms/fastsimSignal%s/RA2bin_signal.root" %model, "READ")
	signal=signalFile.Get("RA2bin_%s_%d_%d_fast" %(model,mGo, mLSP))
	
	signal.Scale(7600)
	DataHist.SetBinErrorOption(ROOT.TH1F.kPoisson);
	DataHist.SetMarkerColor(1);
	DataHist.SetMarkerStyle(20);
	DataHist.SetMarkerSize(2);	
	DataHist.SetLineColor(1);
	#DataHist.SetLineWidth(2.2);
	signal.SetMarkerColor(2);
	signal.SetMarkerStyle(24);
	signal.SetMarkerSize(2);	
		
	qcd_uscb_gold = TColor (2001, 255/255.,200/255.,47/255);
	znn_penn_red = TColor(2002, 255/255.,0/255.,43/255.);
	lost_lep_dusk_blue = TColor(2006, 105/255.,166/255., 202/255.);
	had_tau_grayed_jade = TColor(2007, 133/255.,189/255., 164/255.);

	histqcd.SetFillColor(2001);
	# histqcd.SetLineColor(kYellow);
	histZ.SetFillColor(2002);
	# histZ.SetLineColor(kCyan);
	histLL.SetFillColor(2006);
	# histLL.SetLineColor(kBlue);
	histTau.SetFillColor(2007);
	# histTau.SetLineColor(kGreen);
	hsprefit = THStack();
	hsprefit.Add(histZ);
	hsprefit.Add(histqcd);
	hsprefit.Add(histLL);
	hsprefit.Add(histTau);
	hsprefit_tot = hsprefit.GetStack().Last();
	hsprefit_tot.SetMarkerStyle(24);
	hsprefit_tot.SetMarkerSize(2);
	hsprefit_tot.SetMarkerColor(2);
	hsprefit_tot.SetLineColor(2);
	canPre = TCanvas("canPre","canPre",1600,800);
	hsprefit.Draw('hist');
	leg = TLegend(0.55,0.6,0.9,0.87);
	leg.SetFillStyle(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(0.04);	
	leg.AddEntry(DataHist,"Data","pe")
	leg.AddEntry(hsprefit_tot,"Pre-fit total background","f")
	leg.AddEntry(histqcd,"QCD","f")
	leg.AddEntry(histZ,"Z#rightarrow#nu#bar{#nu}","f")
	leg.AddEntry(histTau,"Hadronic #tau lepton","f")
	leg.AddEntry(histLL,"Lost lepton","f")	
	leg.AddEntry(signal, "Signal T1tttt(1200,800) " , "p")
	leg.Draw()
	DataHist.Draw("psame")
	canPre.SetLogy()	
	canPre.Print("PreFitPlot7.6fb.pdf")
	canPostAN = TCanvas("canPostAN","canPostAN",1600,1200);
	canPostAN.Divide(1,3)
	canPostAN.cd(1)
	leg.Draw()
	DataDiff=DataHist.Clone("DataDiff")
	QValue = TH1F('Qvalue','Q',160,0.5,160.5);
	QValue.GetYaxis().SetTitle("Q")	
	Qsr=0
	PrefitErrorUp=[]
        PrefitErrorDn=[]
	fprefit=open("ParsedInputPrefit.txt", 'r')
	for line in fprefit:
		parse=line.split(" ")
		PrefitErrorUp.append(float(parse[2]))
                PrefitErrorDn.append(float(parse[3]))
	print "bin & Q & Signal & Total Bkg. & Obs. & Sigma \\\\"
	Totalq2=0
	dictQ={}
	for i in range(1,161):
		s=signal.GetBinContent(i)
                b=hsprefit_tot.GetBinContent(i)
                q=2*(sqrt(s+b)-sqrt(b))
		Totalq2=Totalq2+(q*q)
		dictQ[i]=q*q
	sortedQbins=sorted(dictQ.items(), key=operator.itemgetter(1))	
	sortedQbins.reverse()
	#print sortedQbins
	HighestBins=[]
	for i in range(1,161):
                s=signal.GetBinContent(i)
                b=hsprefit_tot.GetBinContent(i)
                q=2*(sqrt(s+b)-sqrt(b))
		binlabel=signal.GetXaxis().GetBinLabel(i)
		QValue.SetBinContent(i, q)
	fractionalQ=0
	cutoff=0.7
	for ibin in sortedQbins:
		fractionalQ=fractionalQ+(QValue.GetBinContent(ibin[0])*QValue.GetBinContent(ibin[0]))
		if fractionalQ/Totalq2>cutoff:break
		i=ibin[0]
		s=signal.GetBinContent(i)
                b=hsprefit_tot.GetBinContent(i)
		q=QValue.GetBinContent(ibin[0])
		Pull=Pull=DataHist.GetBinContent(i)-hsprefit_tot.GetBinContent(i)
		if Pull>=0:
                        if DataHist.GetBinContent(i)>0.0:
                         	Pull=Pull/sqrt(DataHist.GetBinContent(i)+(PrefitErrorUp[i-1]*PrefitErrorUp[i-1]))
			else: Pull=Pull/sqrt(1+(PrefitErrorUp[i-1]*PrefitErrorUp[i-1]))	
                else:
                         if DataHist.GetBinContent(i)>0.0:
                                Pull=Pull/sqrt(DataHist.GetBinContent(i)+(PrefitErrorDn[i-1]*PrefitErrorDn[i-1]))
			 else:
				Pull=Pull/sqrt(1.0+(PrefitErrorDn[i-1]*PrefitErrorDn[i-1]))
                DataDiff.SetBinContent(i, Pull)
		print "%d  & %1.2f & %2.2f & %2.2f & %g & %g \\\\ "   %(i,q, s, b,  DataHist.GetBinContent(i), Pull)
	print fractionalQ,fractionalQ/Totalq2
	'''	

	for i in range(1,161):
		Pull=DataHist.GetBinContent(i)-hsprefit_tot.GetBinContent(i)
		if Pull>=0:
			if PrefitErrorUp[i-1]>0.0 or DataHist.GetBinContent(i)>0.0:
				Pull=Pull/sqrt(DataHist.GetBinContent(i)+(PrefitErrorUp[i-1]*PrefitErrorUp[i-1]))
		else:
			 if PrefitErrorDn[i-1]>0.0 or DataHist.GetBinContent(i)>0.0:
				Pull=Pull/sqrt(DataHist.GetBinContent(i)+(PrefitErrorDn[i-1]*PrefitErrorDn[i-1]))
		DataDiff.SetBinContent(i, Pull)
		if(q>0.5):
			Qsr=Qsr+(q*q)
			print "%d  & %1.2f & %2.2f & %2.2f & %g & %g \\\\ "   %(i,q, s, b,  DataHist.GetBinContent(i), Pull)
			#print " bin %d %s  & Qval %1.2f Signal %2.2f Total Background %2.2f Obs %g  Sigma %g" %(i,binlabel,q, s, b,  DataHist.GetBinContent(i), Pull) 			
	'''
	DataDiff.GetYaxis().SetTitle("(Data-Pre-fit Bkg)/(#sigma_{sys}+#sigma_{data})")
	DataDiff.GetYaxis().SetRangeUser(-5,5)
	DataDiff.Draw("p");
	signal=DataHist.Clone("signal")
	for i in range(1,161):
		if(QValue.GetBinContent(i)>0.2):
			signal.SetBinContent(i,  (QValue.GetBinContent(i)/QValue.Integral()) *DataDiff.GetBinContent(i))
		else:
			signal.SetBinContent(i,0)
	canPostAN.cd(3)
	signal.GetYaxis().SetTitle("(Data-Pre-fit Bkg) Weighted by QValue")
	signal.Draw("p")
	
	canPostAN.cd(2)
	QValue.Draw("")
	canPostAN.Print("QValueDataPull_%s_%d_%d.pdf" %(model,mGo, mLSP))

	#canPostAN.Print("TestQValue.C")
	#canPostAN.Print("StackBkgT1tttt1200_900.pdf")
	canPostAN2 = TCanvas("canPostAN2","canPostAN",1600,1200);
	canPostAN2.cd()
	QValue.Draw("")
	canPostAN2.Print("QValue%s%d_%d.pdf" %(model,mGo, mLSP))

