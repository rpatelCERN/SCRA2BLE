import os
from ROOT import *
finMCBkg=TFile("BkgInputCards.root", "READ")
ZinvMC=finMCBkg.Get("ZInvBkgSR")
DYZllMC=finMCBkg.Get("DYControl")
GJetsMC=finMCBkg.Get("GJetsControl")
finQCD=TFile("../histograms_35.9fb/QcdPredictionRandS.root", "READ")
finZinv=TFile("../histograms_35.9fb/ZinvHistos.root", "READ")
ZinvBGpred=finZinv.Get("ZinvBGpred")
hzvvTF=finZinv.Get("hzvvTF")
hzvvTF.Reset()
finLLHad=TFile("../histograms_35.9fb/InputsForLimits_data_formatted_LLPlusHadTau.root", "READ")
finZinv.Get("")
GJetsTemplate=finZinv.Get("hzvvgJNobs");
hzvvgJNobs=GJetsTemplate.Clone("hzvvgJNobs")
hzvvgJNobs.Reset();
ZRatio0b=TH1D("ZRatio0b", "", 46, 1, 47);
Photon0b=TH1D("Photon0b", "", 46, 1, 47);
DYZll0b=TH1D("DYZll0b", "", 5, 1, 6);
DYZll1b=TH1D("DYZll1b", "", 5, 1, 6);
DYZll2b=TH1D("DYZll2b", "", 5, 1, 6);
DYZll3b=TH1D("DYZll3b", "", 5, 1, 6);
ZinvBGpred.Reset();
for i in range(1, 175):
	#print parseSR
	
	CRLabel=GJetsTemplate.GetXaxis().GetBinLabel(i)
	parseCR=CRLabel.split("_")
	#print parseCR
	#GJYield=GJetsMC.GetBinContent(i)
	for j in range(1, 175):#Patch the GJet Control Sample
		SRLabel=GJetsMC.GetXaxis().GetBinLabel(j)
		parseSR=SRLabel.split("_")
		if parseSR[0]==parseCR[1] and parseSR[2]==parseCR[2] and parseSR[3]==parseCR[3] and parseSR[1]=="BTags0": 
			#print parseSR[1]
			GJYield=GJetsMC.GetBinContent(j)
			hzvvgJNobs.SetBinContent(i, GJYield)
			#hzvvgJNobs.GetXaxis().SetBinLabel(i, hzvvgJNobs.GetB)
			#if parseSR[0]=="BTags0":
				#Photon0b.SetBinContent(i, GJYield+Photon0b.GetBinContent(i)		
ZeroBCount=1;
NJetCount=1;
for i in range(1, 175):
	SRLabel=GJetsMC.GetXaxis().GetBinLabel(i)
	ZinvBGpred.GetXaxis().SetBinLabel(i,SRLabel)
	parseSR=SRLabel.split("_")
	if parseSR[1]=="BTags0":
		Photon0b.SetBinContent(ZeroBCount,GJetsMC.GetBinContent(i))
		ZRatio0b.SetBinContent(ZeroBCount, ZinvMC.GetBinContent(i))
		ZeroBCount=ZeroBCount+1
for j in range(0,5):
	for i in range(1, 175):	
		SRLabel=DYZllMC.GetXaxis().GetBinLabel(i)
		parseSR=SRLabel.split("_")
		if parseSR[0]=="NJets%d" %j:
			if parseSR[1]=="BTags0":
				DYZll0b.SetBinContent(j+1, DYZll0b.GetBinContent(j+1)+DYZllMC.GetBinContent(i))
			if parseSR[1]=="BTags1":
	        	        DYZll1b.SetBinContent(j+1, DYZll1b.GetBinContent(j+1)+DYZllMC.GetBinContent(i))
			if parseSR[1]=="BTags2":
       				DYZll2b.SetBinContent(j+1, DYZll2b.GetBinContent(j+1)+DYZllMC.GetBinContent(i))
			if parseSR[1]=="BTags3":
        	        	DYZll3b.SetBinContent(j+1, DYZll3b.GetBinContent(j+1)+DYZllMC.GetBinContent(i))
ZRatio0b.Divide(Photon0b);#Zgamma Ratio
BExtrap0b=DYZll0b.Clone("BExtrap0b");
BExtrap0b.Divide(DYZll0b)#trivially 1
BExtrap1b=DYZll1b.Clone("BExtrap1b");
BExtrap1b.Divide(DYZll0b);
BExtrap2b=DYZll2b.Clone("BExtrap2b");
BExtrap2b.Divide(DYZll0b);
BExtrap3b=DYZll3b.Clone("BExtrap3b");
BExtrap3b.Divide(DYZll0b);
#high NJet ratio
HighestJetBin=DYZll1b.Clone("HighestJetBin");
HighestJetBin.Add(DYZll0b)
HighestJetBin.Add(DYZll2b)
HighestJetBin.Add(DYZll3b)
HighNJetExtrap=HighestJetBin.GetBinContent(5)/HighestJetBin.GetBinContent(4)
print HighNJetExtrap
ZeroBCount=1;
OneBCount=1;
TwoBCount=1;
MultiBCount=1;
for i in range(1, 175):
        SRLabel=GJetsMC.GetXaxis().GetBinLabel(i)
        parseSR=SRLabel.split("_")
	BExtrap=1.0
	if parseSR[1]=="BTags0":
		for j in range(0,5):
			if parseSR[0]=="NJets%d" %j:BExtrap=BExtrap0b.GetBinContent(j+1)
                ZGammaRatio=ZRatio0b.GetBinContent(ZeroBCount);
                Zpred=ZGammaRatio*BExtrap*Photon0b.GetBinContent(ZeroBCount);
		ZinvBGpred.SetBinContent(i,Zpred);
		#hzvvTF.SetBinContent(i,ZGammaRatio*BExtrap);
                #print Zpred,ZinvMC.GetBinContent(i)
                ZeroBCount=ZeroBCount+1

for i in range(1, 175):
        SRLabel=GJetsMC.GetXaxis().GetBinLabel(i)
        parseSR=SRLabel.split("_")
        BExtrap=1.0
        if parseSR[1]=="BTags1":
		for j in range(0,5):
			if parseSR[0]=="NJets%d" %j:BExtrap=BExtrap1b.GetBinContent(j+1)
		ZGammaRatio=ZRatio0b.GetBinContent(OneBCount);
		ZeroBBinLabel=parseSR[0]+"_BTags0"+"_"+parseSR[2]+"_"+parseSR[3]
		ZeroPhotonPrediction=ZinvMC.GetBinContent(ZinvMC.GetXaxis().FindBin(ZeroBBinLabel))
		#Zpred=ZGammaRatio*BExtrap*Photon0b.GetBinContent(OneBCount);
		Zpred=BExtrap*ZeroPhotonPrediction;
		ZinvBGpred.SetBinContent(i,Zpred);
		#hzvvTF.SetBinContent(i,ZGammaRatio*BExtrap);
		#if(hzvvTF.GetBinContent(i)<=0.0): hzvvTF.SetBinContent(i,ZGammaRatio);
		#print SRLabel,ZeroBBinLabel,Zpred,ZinvMC.GetBinContent(i)
		#print Zpred,ZinvMC.GetBinContent(i)
		OneBCount=OneBCount+1
        if parseSR[1]=="BTags2":
		for j in range(0,5):
			if parseSR[0]=="NJets%d" %j:BExtrap=BExtrap2b.GetBinContent(j+1)
		ZGammaRatio=ZRatio0b.GetBinContent(TwoBCount);
		ZeroBBinLabel=parseSR[0]+"_BTags0"+"_"+parseSR[2]+"_"+parseSR[3]
		ZeroPhotonPrediction=ZinvMC.GetBinContent(ZinvMC.GetXaxis().FindBin(ZeroBBinLabel))
		Zpred=ZeroPhotonPrediction*BExtrap#ZGammaRatio*BExtrap*Photon0b.GetBinContent(MultiBCount);
		ZinvBGpred.SetBinContent(i,Zpred);
		#hzvvTF.SetBinContent(i,ZGammaRatio*BExtrap);
		#if(hzvvTF.GetBinContent(i)<=0.0): hzvvTF.SetBinContent(i,ZGammaRatio);
		#print SRLabel,Photon0b.GetBinContent(TwoBCount),BExtrap,Zpred,ZinvMC.GetBinContent(i)
		TwoBCount=TwoBCount+1
        if parseSR[1]=="BTags3":
		for j in range(0,5):
			if parseSR[0]=="NJets%d" %j:BExtrap=BExtrap3b.GetBinContent(j+1)
		ZGammaRatio=ZRatio0b.GetBinContent(MultiBCount);
		ZeroBBinLabel=parseSR[0]+"_BTags0"+"_"+parseSR[2]+"_"+parseSR[3]
		ZeroPhotonPrediction=ZinvMC.GetBinContent(ZinvMC.GetXaxis().FindBin(ZeroBBinLabel))
		Zpred=ZeroPhotonPrediction*BExtrap#ZGammaRatio*BExtrap*Photon0b.GetBinContent(MultiBCount);
		ZinvBGpred.SetBinContent(i,Zpred);
		#hzvvTF.SetBinContent(i,ZGammaRatio*BExtrap);
		#if(hzvvTF.GetBinContent(i)<=0.0): hzvvTF.SetBinContent(i,ZGammaRatio);
		#print SRLabel,Zpred,ZinvMC.GetBinContent(i)
		MultiBCount=MultiBCount+1
for i in range(1, 175):
	SRLabel=GJetsMC.GetXaxis().GetBinLabel(i)
	parseSR=SRLabel.split("_")
	if parseSR[0]=="NJets4" and parseSR[1]!="BTags0":
		LowerNJetBinLabel="NJets3"+"_"+parseSR[1]+"_"+parseSR[2]+"_"+parseSR[3]
		LowerNJetBin=ZinvBGpred.GetXaxis().FindBin(LowerNJetBinLabel)	
		LowerNJetPred=ZinvBGpred.GetBinContent(LowerNJetBin)
		#if hzvvTF.GetBinContent(i)!=0:
		 
		#hzvvTF.SetBinContent(i,hzvvTF.GetBinContent(i)*HighNJetExtrap);
		#else: hzvvTF.SetBinContent(i,HighNJetExtrap);
		ZinvBGpred.SetBinContent(i,LowerNJetPred*HighNJetExtrap)
		#print SRLabel,hzvvTF.GetXaxis().GetBinLabel(i)
		#print HighNJetExtrap*LowerNJetPred, ZinvMC.GetBinContent(i)
		#print LowerNJetBinLabel,SRLabel,LowerNJetPred*HighNJetExtrap,ZinvMC.GetBinContent(i)
for i in range(1, 175):
	TF= ZinvBGpred.GetBinContent(i)/hzvvgJNobs.GetBinContent(i)
	hzvvTF.SetBinContent(i, TF);
fout=TFile("ZinvHistos.root","RECREATE")
fout.cd()
hzvvgJNobs.Write("hzvvgJNobs");
ZSys=["hzvvNbCorrelUp", "hzvvNbCorrelLow", "hzvvgJEtrgErr", "hgJFdirErrUp", "hgJFdirErrLow", "hzvvgJPurErr", "hzvvScaleErr", "hzvvDYstat", "hzvvDYsysPur", "hzvvDYsysKin","hzvvDYMCerrUp","hzvvDYMCerrLow"]
ZinvBGpred.Write("ZinvBGpred");
hzvvTF.Write("hzvvTF")
for z in ZSys:
	finZinv.Get(z).Write(z);
fout2=TFile("InputsForLimits_data_formatted_LLPlusHadTau.root","RECREATE")
fout2.cd()
SLTF=finMCBkg.Get("TFSingleLepton")
SLCS=finMCBkg.Get("SLControl")
for i in range(1, 175):
	SLTF.GetXaxis().SetBinLabel(i, "LLPlusHadTauTF_"+SLTF.GetXaxis().GetBinLabel(i))
	SLCS.GetXaxis().SetBinLabel(i, SLTF.GetXaxis().GetBinLabel(i))
SLTF.Write("LLPlusHadTauTF")
SLCS.Write("DataCSStatistics")

finMCBkg.Get("SLBkgSR").Write("totalPred_LLPlusHadTau")

LLHadSys=["LLPlusHadTauTFErr","DataCSStatErr", "totalPredBMistagDown_LLPlusHadTau", "totalPred_JECSysDown_LLPlusHadTau", "totalPredMTWSysDown_LLPlusHadTau", "totalPredLepAccSysDown_LLPlusHadTau",
"totalPredLepAccQsquareSysDown_LLPlusHadTau", "totalPredMuIsoSysDown_LLPlusHadTau", "totalPredMuRecoSysDown_LLPlusHadTau"]
for l in LLHadSys:
	finLLHad.Get(l).Write(l);
fout3=TFile("QcdPredictionRandS.root","RECREATE")
fout3.cd()
finMCBkg.Get("QCDBkgSR").Write("PredictionCV")
QCDSyst=["PredictionCoreUp", "PredictionTail", "PredictionBTag","hPredictionUncorrelated"]
for q in QCDSyst:
	finQCD.Get(q).Write(q);
