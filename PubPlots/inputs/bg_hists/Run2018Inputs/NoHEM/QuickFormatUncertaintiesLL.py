import os
from ROOT import *
import math
from array import array
finZinv=TFile("InputsForLimits_data_formatted_LLPlusHadTau_PreHEMRecheck.root", "READ")
hzvvgJNobs=finZinv.Get("DataCSStatistics")
hTF=finZinv.Get("LLPlusHadTauTF")
finMC=TFile("../../../signal_hists/inputHistograms/FullSIM/RA2bin_proc_T1bbbb_1000_900_MC2017.root", "READ")
MCBinLabels=finMC.Get("RA2bin_T1bbbb_1000_900_MC2017_nominal");
foutGJ=TFile("LLPreNoHEM.root", "RECREATE")
#zvvgJNobs.Reset();
a_MHT= array('d', [300,350,600,850,2100]);
MHTSignal=TH1F('MHTSignal', ";MHT;Yields", 4,a_MHT)
MHTTF=TH1F('MHTTF', ";MHT;Yields", 4,a_MHT)

#Photon0b=TH1D("Photon0b", "", 46, 1, 47);
#ZinvBGpred.Reset();
TotalPhotonYield=0;
PhotonYieldMHT0=0;
PhotonYieldMHT1=0;
PhotonYieldMHT2=0;
PhotonYieldMHT3=0;
AvgTFMHT0=0;
AvgTFMHT1=0;
AvgTFMHT2=0;
AvgTFMHT3=0;
MHT0Count=0;
MHT1Count=0;
MHT2Count=0;
MHT3Count=0;
BCount=0;
for j in range(1, 175):#Patch the GJet Control Sample
		SRLabel=MCBinLabels.GetXaxis().GetBinLabel(j)
		parseSR=SRLabel.split("_")
		#print parseSR
		GJYield=hzvvgJNobs.GetBinContent(j)
		AvgTF=hTF.GetBinContent(j)
		#if parseSR[0]==parseCR[1] and parseSR[2]==parseCR[2] and parseSR[3]==parseCR[3] and parseSR[1]=="BTags0": 
		#if parseSR[1]=="BTags0" and not parseSR[0]=="NJets4": 
			#print parseSR[1]
		if parseSR[2]=="MHT0":
				PhotonYieldMHT0=PhotonYieldMHT0+GJYield
				AvgTFMHT0=AvgTF+AvgTFMHT0;
				MHT0Count=MHT0Count+1;
		if parseSR[2]=="MHT1":
				PhotonYieldMHT1=PhotonYieldMHT1+GJYield
				AvgTFMHT1=AvgTF+AvgTFMHT1;
				MHT1Count=MHT0Count+1;
		if parseSR[2]=="MHT2":
				PhotonYieldMHT2=PhotonYieldMHT2+GJYield
				AvgTFMHT2=AvgTF+AvgTFMHT2;
				MHT2Count=MHT0Count+1;
		if parseSR[2]=="MHT3":
				PhotonYieldMHT3=PhotonYieldMHT3+GJYield
				AvgTFMHT3=AvgTF+AvgTFMHT3;
				MHT3Count=MHT0Count+1;
			#Yields0b.SetBinContent(BCount, GJYield)
AvgTFMHT0=AvgTFMHT0/MHT0Count	
AvgTFMHT1=AvgTFMHT1/MHT1Count	
AvgTFMHT2=AvgTFMHT2/MHT2Count	
AvgTFMHT3=AvgTFMHT3/MHT3Count	
MHTTF.SetBinContent(1,AvgTFMHT0)			
MHTTF.SetBinContent(2,AvgTFMHT1)			
MHTTF.SetBinContent(3,AvgTFMHT2)			
MHTTF.SetBinContent(4,AvgTFMHT3)	

MHTSignal.SetBinContent(1,PhotonYieldMHT0)			
MHTSignal.SetBinContent(2,PhotonYieldMHT1)			
MHTSignal.SetBinContent(3,PhotonYieldMHT2)			
MHTSignal.SetBinContent(4,PhotonYieldMHT3)	
print PhotonYieldMHT3
foutGJ.cd()
MHTTF.Write("avgTFNoHEM");		
MHTSignal.Write("LLNoHEM");		

