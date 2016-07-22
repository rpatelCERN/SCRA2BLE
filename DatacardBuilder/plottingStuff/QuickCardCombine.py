import os
from ROOT import *

fsig=TFile("../inputHistograms/FullSim/RA2bin_signal.root", "READ")
sighist=fsig.Get("RA2bin_SMSqqqq1400")
sigCards=""
SLCards=""
LDPCards=""
LowMHTLDPCards=""
LowMHTHDPCards=""
for i in range(0,160):
	label=sighist.GetXaxis().GetBinLabel(i+1)
	parse=label.split('_')
	if "BTags0" in parse[1] or "BTags1" in parse[1]:
		sigCards=sigCards+"card_signal%d.txt "   %i
		SLCards=SLCards+"card_SLControl%d.txt "  %i
		LDPCards=LDPCards+"card_Lowdphi%d.txt " %i	
fqcd=open("../inputHistograms/histograms_0.8fb/qcdLowMHT-bg-combine-input.txt", 'r')
PhotonCards=""
for i in range(0,40): PhotonCards=PhotonCards+ "card_sphoton%d.txt " %i
count=0
for line in fqcd:
	parse=line.split('\t')
	label=parse[0]
	Btag=label.split('_')
	if "BTags0" in Btag[1] or "BTags1" in Btag[1]:
		LowMHTLDPCards=LowMHTLDPCards+"card_LowdPhiLowMHT%d.txt " %count
		LowMHTHDPCards=LowMHTLDPCards+"card_HighdPhiLowMHT%d.txt " %count
	count=count+1
os.system("combineCards.py %s %s %s %s %s %s >Cards80bin.txt" %(sigCards, SLCards, LDPCards, LowMHTLDPCards, LowMHTHDPCards,PhotonCards))
