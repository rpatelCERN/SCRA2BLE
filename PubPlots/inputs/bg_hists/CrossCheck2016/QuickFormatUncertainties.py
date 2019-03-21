import os
from ROOT import *
import math
from array import array
fDataUnblind=TFile("../../data_hists/data_fixhtratio/RA2bin_signal.root","READ")
SearchData=fDataUnblind.Get("RA2bin_data2016");
finZinv=TFile("zinvData_2019Feb22_2016/ZinvHistos.root", "READ")
SearchZ=finZinv.Get("ZinvBGpred");

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
NBcorrelUp=finZinv.Get("hzvvNbCorrelUp")
NBcorrelLow=finZinv.Get("hzvvNbCorrelLow")
hzvvgJNobs=GJetsTemplate.Clone("hzvvgJNobs")
finMC=TFile("../../signal_hists/T1tttt_hists.root", "READ")
MCBinLabels=finMC.Get("RA2bin_T1tttt_1200_800_fast_nominal");
foutGJ=TFile("GJets_2016.root", "RECREATE")
#zvvgJNobs.Reset();
Yields0b=TH1D("ZRatio0b", "", 46, 1, 47);

a_MHT= array('d', [300,350,600,850,2100]);
MHTSignal=TH1F('MHTSignal', ";MHT;Yields", 4,a_MHT)
UnblindMHTSignal=TH1F('UnblindMHTSignal', ";MHT;Yields", 4,a_MHT)

#Photon0b=TH1D("Photon0b", "", 46, 1, 47);
#ZinvBGpred.Reset();
TotalPhotonYield=0;
PhotonYieldMHT0=0;
PhotonYieldMHT1=0;
PhotonYieldMHT2=0;
PhotonYieldMHT3=0;

METYieldMHT0=0;
METYieldMHT1=0;
METYieldMHT2=0;
METYieldMHT3=0;


METZYieldMHT0=0;
METZYieldMHT1=0;
METZYieldMHT2=0;
METZYieldMHT3=0;


METYieldMHT0Unc=0;
METYieldMHT1Unc=0;
METYieldMHT2Unc=0;
METYieldMHT3Unc=0;
BCount=0;
DumbBinNumbers=[]
for j in range(1, 175):#Patch the GJet Control Sample
		SRLabel=MCBinLabels.GetXaxis().GetBinLabel(j)
		parseSR=SRLabel.split("_")
		print parseSR
		#if parseSR[0]==parseCR[1] and parseSR[2]==parseCR[2] and parseSR[3]==parseCR[3] and parseSR[1]=="BTags0": 
		if parseSR[1]=="BTags2" or parseSR[1]=="BTags3": #and not parseSR[0]=="NJets4": 
			DumbBinNumbers.append(j)
		if parseSR[1]=="BTags0": #and not parseSR[0]=="NJets4": 
			
			#print parseSR[1]
			GJYield=GJetsTemplate.GetBinContent(j)
			PhotonSF=BetaPurity.GetBinContent(j)
			if parseSR[2]=="MHT0":
				PhotonYieldMHT0=PhotonYieldMHT0+GJYield*PhotonSF
			if parseSR[2]=="MHT1":
				PhotonYieldMHT1=PhotonYieldMHT1+GJYield*PhotonSF
			if parseSR[2]=="MHT2":
				PhotonYieldMHT2=PhotonYieldMHT2+GJYield*PhotonSF
			if parseSR[2]=="MHT3":
				PhotonYieldMHT3=PhotonYieldMHT3+GJYield*PhotonSF
		if parseSR[1]=="BTags0":
			if parseSR[2]=="MHT0":
				METYieldMHT0=METYieldMHT0+SearchData.GetBinContent(j)
				METZYieldMHT0=METZYieldMHT0+SearchZ.GetBinContent(j)
				METYieldMHT0Unc=METYieldMHT0Unc+SearchZ.GetBinContent(j)*(1.0-NBcorrelLow.GetBinContent(j))
			if parseSR[2]=="MHT1":
				METYieldMHT1=METYieldMHT1+SearchData.GetBinContent(j)
				METZYieldMHT1=METZYieldMHT1+SearchZ.GetBinContent(j)
				METYieldMHT1Unc=METYieldMHT1Unc+SearchZ.GetBinContent(j)*(1.0-NBcorrelLow.GetBinContent(j))
			if parseSR[2]=="MHT2":
				METYieldMHT2=METYieldMHT2+SearchData.GetBinContent(j)
				METZYieldMHT2=METZYieldMHT2+SearchZ.GetBinContent(j)
				METYieldMHT2Unc=METYieldMHT2Unc+SearchZ.GetBinContent(j)*(1.0-NBcorrelLow.GetBinContent(j))
			if parseSR[2]=="MHT3":
				METYieldMHT3=METYieldMHT3+SearchData.GetBinContent(j)
				METZYieldMHT3=METZYieldMHT3+SearchZ.GetBinContent(j)
				METYieldMHT3Unc=METYieldMHT3Unc+SearchZ.GetBinContent(j)*(1.0-NBcorrelLow.GetBinContent(j))*2.0
			
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
			#print "%d & %d & $%.3f\pm %.3f$ & $%.3f\pm%.3f$ & $%.3f^{+%.3f}_{-%.3f}$ & $%.3f^{+%.3f}_{-%.3f}$ & $%.1f\pm %.1f$\\\\" %(BCount, GJYield, Purity,PError, RZg,RZgE,FDir,FDirUp,FDirDown, Rho,RhoUp, RhoDown, GJYield*Purity*RZg*FDir*Rho,StatUnc*Purity*RZg*FDir*Rho )

			#Yields0b.SetBinContent(BCount, GJYield)
MHTSignal.SetBinContent(1,PhotonYieldMHT0)			
MHTSignal.SetBinContent(2,PhotonYieldMHT1)			
MHTSignal.SetBinContent(3,PhotonYieldMHT2)			
MHTSignal.SetBinContent(4,PhotonYieldMHT3)	
UnblindMHTSignal.SetBinContent(1,METYieldMHT0)
UnblindMHTSignal.SetBinContent(2,METYieldMHT1)
UnblindMHTSignal.SetBinContent(3,METYieldMHT2)
UnblindMHTSignal.SetBinContent(4,METYieldMHT3)

foutGJ.cd()
MHTSignal.Write("GJets2016");
UnblindMHTSignal.Write("Unblind2016");	
#print BCount,METYieldMHT0,METYieldMHT0Unc,METYieldMHT1,METYieldMHT2,METYieldMHT3
print DumbBinNumbers
#print BCount,METZYieldMHT3,METYieldMHT3Unc
#print BCount,PhotonYieldMHT0,PhotonYieldMHT1,PhotonYieldMHT2,PhotonYieldMHT3
