import os
from ROOT import *
import math
from array import array
finZinv=TFile("RA2bin_signal.root", "READ")
hzvvgJNobs=finZinv.Get("RA2bin_data2018")
finMC=TFile("../../signal_hists/T1tttt_hists.root", "READ")
MCBinLabels=finMC.Get("RA2bin_T1tttt_1200_800_fast_nominal");
foutGJ=TFile("DataNoHEM.root", "RECREATE")
#zvvgJNobs.Reset();
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
		GJYield=hzvvgJNobs.GetBinContent(j)
		#if parseSR[0]==parseCR[1] and parseSR[2]==parseCR[2] and parseSR[3]==parseCR[3] and parseSR[1]=="BTags0": 
		#if parseSR[1]=="BTags0" and not parseSR[0]=="NJets4": 
			#print parseSR[1]
		if parseSR[2]=="MHT0":
				PhotonYieldMHT0=PhotonYieldMHT0+GJYield
		if parseSR[2]=="MHT1":
				PhotonYieldMHT1=PhotonYieldMHT1+GJYield
		if parseSR[2]=="MHT2":
				PhotonYieldMHT2=PhotonYieldMHT2+GJYield
		if parseSR[2]=="MHT3":
				PhotonYieldMHT3=PhotonYieldMHT3+GJYield
			
			#Yields0b.SetBinContent(BCount, GJYield)
MHTSignal.SetBinContent(1,PhotonYieldMHT0)			
MHTSignal.SetBinContent(2,PhotonYieldMHT1)			
MHTSignal.SetBinContent(3,PhotonYieldMHT2)			
MHTSignal.SetBinContent(4,PhotonYieldMHT3)	
foutGJ.cd()
MHTSignal.Write("DataNoHEM");		
