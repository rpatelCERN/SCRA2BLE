from ROOT import *

#fin=TFile("BkgInputCards_135000pb-nominal.root", "READ")
fin=TFile("BkgInputCards.root", "READ")
GJetsControl=fin.Get("GJetsControl")
DYControl=fin.Get("DYControl")
SLControl=fin.Get("SLControl")
for i in range(1,174):
	SRLabel=GJetsControl.GetXaxis().GetBinLabel(i)
	if GJetsControl.GetBinContent(i)==0:
		print "GJets CS is zero in bin %s " %SRLabel
	if DYControl.GetBinContent(i)==0:
		print "DY CS is zero in bin %s " %SRLabel
	#if SLControl.GetBinContent(i)==0:
		#print "SL CS is zero in bin %s " %SRLabel
