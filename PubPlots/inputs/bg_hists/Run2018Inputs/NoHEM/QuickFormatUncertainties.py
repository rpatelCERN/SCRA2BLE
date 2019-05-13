import os
from ROOT import *
import math
from array import array
finZinv=TFile("ZinvHistos.root", "READ")
GJetsTemplate=finZinv.Get("hzvvgJNobs");
BetaPurity=finZinv.Get("hgJPur");
BetaPurityError=finZinv.Get("hzvvgJPurErr");
RZgamma=finZinv.Get("hgJZgR");
RZgammaError=finZinv.Get("hgJZgRerr");
PhotonFrac=finZinv.Get("hgJFdir");
FDirErrorUp=finZinv.Get("hgJFdirErrUp");
FDirErrorDown=finZinv.Get("hgJFdirErrLow");
DoubleRatioRho=finZinv.Get("hZgDR");
DRErrorUp=finZinv.Get("hZgDRerrUp");
DRErrorDown=finZinv.Get("hZgDRerrLow");

hzvvgJNobs=GJetsTemplate.Clone("hzvvgJNobs")
finMC=TFile("../../../signal_hists/T1tttt_hists.root", "READ")
MCBinLabels=finMC.Get("RA2bin_T1tttt_1200_800_fast_nominal");
foutGJ=TFile("GJets_2016.root", "RECREATE")
#zvvgJNobs.Reset();
Yields0b=TH1D("ZRatio0b", "", 46, 1, 47);

a_MHT= array('d', [300,350,600,850,2100]);
MHTSignal=TH1F('MHTSignal', ";MHT;Yields", 4,a_MHT)

#Photon0b=TH1D("Photon0b", "", 46, 1, 47);
#ZinvBGpred.Reset();
TotalPhotonYield=0;
PhotonYieldMHT0=0;
PhotonYieldMHT1=0;
PhotonYieldMHT2=0;
PhotonYieldMHT3=0;

BCount=0;
for j in range(1, 175):#Patch the GJet Control Sample
		SRLabel=MCBinLabels.GetXaxis().GetBinLabel(j)
		parseSR=SRLabel.split("_")
		print parseSR
		#if parseSR[0]==parseCR[1] and parseSR[2]==parseCR[2] and parseSR[3]==parseCR[3] and parseSR[1]=="BTags0": 
		if parseSR[1]=="BTags0" and not parseSR[0]=="NJets4": 
			#print parseSR[1]
			GJYield=GJetsTemplate.GetBinContent(j)
			if parseSR[2]=="MHT0":
				PhotonYieldMHT0=PhotonYieldMHT0+GJYield
			if parseSR[2]=="MHT1":
				PhotonYieldMHT1=PhotonYieldMHT1+GJYield
			if parseSR[2]=="MHT2":
				PhotonYieldMHT2=PhotonYieldMHT2+GJYield
			if parseSR[2]=="MHT3":
				PhotonYieldMHT3=PhotonYieldMHT3+GJYield
			TotalPhotonYield=TotalPhotonYield+GJYield;
			StatUnc=GJetsTemplate.GetBinError(j)
			Purity=BetaPurity.GetBinContent(j)
			PError=(BetaPurityError.GetBinContent(j)-1.0)*Purity
			RZg=RZgamma.GetBinContent(j)
			RZgE=(RZgammaError.GetBinContent(j)-1.0)*RZg
			FDir=PhotonFrac.GetBinContent(j)
			FDirUp=FDir*(FDirErrorUp.GetBinContent(j)-1.0)
			FDirDown=FDir*(1.0-FDirErrorDown.GetBinContent(j))
			Rho=DoubleRatioRho.GetBinContent(j)
			RhoUp=(DRErrorUp.GetBinContent(j)-1.0)*Rho
			RhoDown=(1.0-DRErrorDown.GetBinContent(j))*Rho
			
			BCount=BCount+1
			print "%d & %d & $%.3f\pm %.3f$ & $%.3f\pm%.3f$ & $%.3f^{+%.3f}_{-%.3f}$ & $%.3f^{+%.3f}_{-%.3f}$ & $%.1f\pm %.1f$\\\\" %(BCount, GJYield, Purity,PError, RZg,RZgE,FDir,FDirUp,FDirDown, Rho,RhoUp, RhoDown, GJYield*Purity*RZg*FDir*Rho,StatUnc*Purity*RZg*FDir*Rho )

			#Yields0b.SetBinContent(BCount, GJYield)
MHTSignal.SetBinContent(1,PhotonYieldMHT0)			
MHTSignal.SetBinContent(2,PhotonYieldMHT1)			
MHTSignal.SetBinContent(3,PhotonYieldMHT2)			
MHTSignal.SetBinContent(4,PhotonYieldMHT3)	
foutGJ.cd()
MHTSignal.Write("GJetsNoHEM");		
print BCount,TotalPhotonYield,PhotonYieldMHT0,PhotonYieldMHT1,PhotonYieldMHT2,PhotonYieldMHT3
