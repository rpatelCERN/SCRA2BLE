import os
from ROOT import *
import math
finZinv=TFile("ZinvHistos_2016.root", "READ")
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
finMC=TFile("../../../../DatacardBuilder/inputHistograms/MCForBinOptimization/RA2bin_proc_T1qqqq_1900_200_fast.root", "READ")
MCBinLabels=finMC.Get("RA2bin_T1qqqq_1900_200_fast_nominal");
#hzvvgJNobs.Reset();
Yields0b=TH1D("ZRatio0b", "", 46, 1, 47);
#Photon0b=TH1D("Photon0b", "", 46, 1, 47);
#ZinvBGpred.Reset();
TotalPhotonYield=0;
BCount=0;
for j in range(1, 175):#Patch the GJet Control Sample
		SRLabel=MCBinLabels.GetXaxis().GetBinLabel(j)
		parseSR=SRLabel.split("_")
		#if parseSR[0]==parseCR[1] and parseSR[2]==parseCR[2] and parseSR[3]==parseCR[3] and parseSR[1]=="BTags0": 
		if parseSR[1]=="BTags0": 
			#print parseSR[1]
			GJYield=GJetsTemplate.GetBinContent(j)
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
			
print BCount,TotalPhotonYield
