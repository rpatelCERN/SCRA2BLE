import os
from ROOT import *
'''
f=open("qcd-bg-combine-input.txt" ,'r');
fout=open("qcd-bg-combine-inputFormatted.txt" ,'w');
count=1
for line in f:
	fout.write(line)
	count=count+1
	if count==31:break
f.seek(0,0)
f.close()
f=open("qcd-bg-combine-input.txt" ,'r');
for line in f:
	#parse=line.split('    ')
	#newparse=parse[0].split(' ')
	#print parse
	#if len(newparse)<5:continue
	if "-HT3" in line and "NJets2" in line:continue
	if "-HT3" in line and "NJets3" in line:continue
	if "-HT0" in line and "NJets2" in line:continue
	if "-HT0" in line and "NJets3" in line:continue
	parse=line.split('    ')
	print parse[1]
	fout.write(line)
fout.close()
'''
fhadtau=TFile("HadTauEstimation_data_formatted.root","READ");
hadtauSearchBin=fhadtau.Get("searchBin_nominal")
hadtauStatUnc=fhadtau.Get("searchBin_StatUncertainties")
hadtauClosure=fhadtau.Get("searchBin_closureUncertainty")
hadtauClosureCorr=fhadtau.Get("searchBin_closureUncertainty_adhoc")
hadtauTrigSys=fhadtau.Get("searchBin_TrigEffUncertainty")
hadtauDiLep=fhadtau.Get("searchBin_DileptonUncertainty")
hadtauMuFromTau=fhadtau.Get("searchBin_MuFromTauStat")
hadtauBmistagUp=fhadtau.Get("searchBin_BMistagUp")
hadtauBmistagDn=fhadtau.Get("searchBin_BMistagDn")
hadtauJECUp=fhadtau.Get("searchBin_JECSysUp")
hadtauJECDn=fhadtau.Get("searchBin_JECSysDn")

hadtauMuRecoUp=fhadtau.Get("searchBin_MuRecoSysUp")
hadtauMuRecoDn=fhadtau.Get("searchBin_MuRecoSysDn")
hadtauMuIsoUp=fhadtau.Get("searchBin_MuIsoSysUp")
hadtauMuIsoDn=fhadtau.Get("searchBin_MuIsoSysDn")
hadtauMuRecoIsoUp=fhadtau.Get("searchBin_MuRecoIsoUp")
hadtauMuRecoIsoDn=fhadtau.Get("searchBin_MuRecoIsoDn")
hadtauMTUp=fhadtau.Get("searchBin_MTSysUp")
hadtauMTDn=fhadtau.Get("searchBin_MTSysDn")
hadtauTkIsoEffStat=fhadtau.Get("searchBin_IsoTrkVetoEffUncertaintyStat")
hadtauTkIsoEffSys=fhadtau.Get("searchBin_IsoTrkVetoEffUncertaintySys")
hadtauMTEffStat=fhadtau.Get("searchBin_MtEffStat")
hadtauAccStat=fhadtau.Get("searchBin_AccStat");
hadtauPDFUp=fhadtau.Get("searchBin_AccSysPDFUp")
hadtauPDFDn=fhadtau.Get("searchBin_AccSysPDFDn")
hadtauPDFScaleUp=fhadtau.Get("searchBin_AccSysScaleUp")
hadtauPDFScaleDn=fhadtau.Get("searchBin_AccSysScaleDn")

ftemplate=TFile("../fastsimSignalT1tttt/RA2bin_signal.root","READ");
Template=ftemplate.Get("RA2bin_T1tttt_1050_300_fast")
LL_file=TFile("LLPrediction.root")
LLMTSys=LL_file.Get("Prediction_data/totalPredMTWSysUp_LL")
LLTkIsoEffSys=LL_file.Get("Prediction_data/totalPredIsoTrackSysUp_LL");
LLMuIso=LL_file.Get("Prediction_data/totalPredMuIsoSysUp_LL")
LLMuReco=LL_file.Get("Prediction_data/totalPredMuRecoSysUp_LL")
LLIsoTrackStat=LL_file.Get("Prediction_data/totalPredIsoTrackStatUp_LL")
LLMuAcc=LL_file.Get("Prediction_data/totalPredMuAccSysUp_LL")
LLMuQScale=LL_file.Get("Prediction_data/totalPredMuAccQsquareSysUp_LL")
LLMuIsoStat=LL_file.Get("Prediction_data/totalPredMuIsoStatUp_LL")
LLMuRecoStat=LL_file.Get("Prediction_data/totalPredMuRecoStatUp_LL")
LLMuAccStat=LL_file.Get("Prediction_data/totalPredMuAccStatUp_LL")
for i in range(1,175):
	binlabel=Template.GetXaxis().GetBinLabel(i)
	hadtauSearchBin.GetXaxis().SetBinLabel(i,binlabel)
	hadtauClosure.GetXaxis().SetBinLabel(i,"HadTauClosure"+binlabel)
	parsenew=binlabel.split('_')
	hadtauClosureCorr.GetXaxis().SetBinLabel(i,"HadTauCorr"+"_"+parsenew[0]+"_"+parsenew[1])
	hadtauBmistagUp.GetXaxis().SetBinLabel(i,"HadTauBMistag")
	hadtauBmistagDn.GetXaxis().SetBinLabel(i,"HadTauBMistag")
	hadtauJECUp.GetXaxis().SetBinLabel(i,"HadTauEScale")
	hadtauJECDn.GetXaxis().SetBinLabel(i,"HadTauEScale")
	hadtauTrigSys.GetXaxis().SetBinLabel(i,"HadTauTrigSyst")
	hadtauDiLep.GetXaxis().SetBinLabel(i,"HadtauDiLep")
	hadtauMuFromTau.GetXaxis().SetBinLabel(i,"HadtauMuFromTau")
	hadtauMuRecoUp.GetXaxis().SetBinLabel(i,LLMuReco.GetXaxis().GetBinLabel(i))			
	hadtauMuRecoDn.GetXaxis().SetBinLabel(i,LLMuReco.GetXaxis().GetBinLabel(i))			
	hadtauMuIsoUp.GetXaxis().SetBinLabel(i,LLMuIso.GetXaxis().GetBinLabel(i))			
	hadtauMuIsoDn.GetXaxis().SetBinLabel(i,LLMuIso.GetXaxis().GetBinLabel(i))			
	hadtauPDFUp.GetXaxis().SetBinLabel(i,LLMuAcc.GetXaxis().GetBinLabel(i))
	hadtauPDFDn.GetXaxis().SetBinLabel(i,LLMuAcc.GetXaxis().GetBinLabel(i))
	hadtauPDFScaleUp.GetXaxis().SetBinLabel(i,LLMuQScale.GetXaxis().GetBinLabel(i))
	hadtauPDFScaleDn.GetXaxis().SetBinLabel(i,LLMuQScale.GetXaxis().GetBinLabel(i))
	hadtauTkIsoEffStat.GetXaxis().SetBinLabel(i,LLMuIsoStat.GetXaxis().GetBinLabel(i))
	hadtauMuRecoIsoUp.GetXaxis().SetBinLabel(i,LLMuRecoStat.GetXaxis().GetBinLabel(i))
	hadtauMuRecoIsoDn.GetXaxis().SetBinLabel(i,LLMuRecoStat.GetXaxis().GetBinLabel(i))
	#print hadtauMuRecoIsoDn.GetXaxis().GetBinLabel(i)
	hadtauAccStat.GetXaxis().SetBinLabel(i,LLMuAccStat.GetXaxis().GetBinLabel(i))
	#hadtauMuRecoIsoUp.GetXaxis().GetBinLabel(i,LLMuIso.GetXaxis().GetBinLabel(i))
	#hadtauMuRecoIsoDn.GetXaxis().GetBinLabel(i,LLMuIso.GetXaxis().GetBinLabel(i))






'''
fzinv=TFile("ZinvHistos.root", "READ");
ftemplate=TFile("../fastsimSignalT1tttt/RA2bin_signal.root","READ");
Template=ftemplate.Get("RA2bin_T1tttt_1050_300_fast")
GJetsHisto=fzinv.Get("hgJNobs")	
GJetsRatioHisto=fzinv.Get("hgJZgR")
GJetsPurHisto=fzinv.Get("hgJPur")
GJetsRatioCorrHisto=fzinv.Get("hgJZgRdataMC");
DY0btoNb=fzinv.Get("hDYvalue")
ZPred=fzinv.Get("ZinvBGpred")

ZGammaErr=fzinv.Get("hgJZgRerr")
PurErr=fzinv.Get("hgJPurErr")
ZgammaErrUp=fzinv.Get("hgJZgRerrUp");
ZgammaErrDn=fzinv.Get("hgJZgRerrLow");
DRErrUp=fzinv.Get("hgJZgRdataMCerrUp")
DRErrDn=fzinv.Get("hgJZgRdataMCerrUp")
DYStat=fzinv.Get("hDYstat")
DYMCStat=fzinv.Get("hDYMCstat")
DYPur=fzinv.Get("hDYsysPur")
DYKin=fzinv.Get("hDYsysKin")
hDYsysNjUp=fzinv.Get("hDYsysNjUp")
hDYsysNjLow=fzinv.Get("hDYsysNjLow")

GJetsHistoNew=Template.Clone()
ZRatios=Template.Clone()
ZPredNew=Template.Clone()

ZGammaErrNew=Template.Clone()
PurErrNew=Template.Clone()
ZgammaErrUpNew=Template.Clone()
ZgammaErrDnNew=Template.Clone()
DRErrUpNew=Template.Clone()
DRErrDnNew=Template.Clone()

DYStatNew=Template.Clone()
DYMCStatNew=Template.Clone()
DYPurNew=Template.Clone()
DYKinNew=Template.Clone()
hDYsysNjUpNew=Template.Clone()
hDYsysNjLowNew=Template.Clone()
for j in range(1,175):
	inputlabel=GJetsHistoNew.GetXaxis().GetBinLabel(j)
	parsenew=inputlabel.split('_')
	binlabel="GJetObsStatErr"+"_"+parsenew[0]+"_"+parsenew[2]+"_"+parsenew[3]
	GJetsHistoNew.GetXaxis().SetBinLabel(j,binlabel)
	binlabel="GJetObsStatErr"+"_"+parsenew[0]+"_"+parsenew[1]+"_"+parsenew[2]+"_"+parsenew[3]
	ZRatios.GetXaxis().SetBinLabel(j,binlabel)
	#print parsenew
	PurErrNew.GetXaxis().SetBinLabel(j, "PhoPur");
	ZgammaErrUpNew.GetXaxis().SetBinLabel(j,"ZgammaRatioErr");
	ZgammaErrDnNew.GetXaxis().SetBinLabel(j,"ZgammaRatioErr");
	DRErrUpNew.GetXaxis().SetBinLabel(j,"DoubleRatioErr"+"_"+parsenew[0]+"_"+parsenew[2]+"_"+parsenew[3])	
	DRErrDnNew.GetXaxis().SetBinLabel(j,"DoubleRatioErr"+"_"+parsenew[0]+"_"+parsenew[2]+"_"+parsenew[3])	
	
	DYKinNew.GetXaxis().SetBinLabel(j,"DYKinemSys"+"_"+parsenew[0]+"_"+parsenew[1]+"_"+parsenew[2]+"_"+parsenew[3])
	DYStatNew.GetXaxis().SetBinLabel(j,"DYStatUnc"+"_"+parsenew[0]+"_"+parsenew[1])
	DYMCStatNew.GetXaxis().SetBinLabel(j,"DYMCStatUnc"+"_"+parsenew[0]+"_"+parsenew[1])
	if(parsenew[1]=="BTags1" or parsenew[1]=="BTags0"):DYPurNew.GetXaxis().SetBinLabel(j,"DYPurUnc"+"_"+parsenew[1])
	if(parsenew[1]=="BTags2" or parsenew[1]=="BTags3"):DYPurNew.GetXaxis().SetBinLabel(j,"DYPurUnc"+"_BTags2Plus")
	hDYsysNjUpNew.GetXaxis().SetBinLabel(j,"DYNjExtrapSys")
	hDYsysNjLowNew.GetXaxis().SetBinLabel(j,"DYNjExtrapSys")
lumiscale=24900./12900.
for i in range(1,175):
	inputlabel=GJetsHistoNew.GetXaxis().GetBinLabel(i)
	parsenew=inputlabel.split('_')
	for j in range(1,160):
	        inputlabel2=GJetsHisto.GetXaxis().GetBinLabel(j)
		if "BTags0" not in inputlabel2:continue
		parsenew2=inputlabel2.split('-')
		#print parsenew2, parsenew
		if parsenew[1]=="NJets0" and parsenew2[0]=="NJets0" and parsenew[2]==parsenew2[2] and parsenew[3]==parsenew2[3]:
			GJetsHistoNew.SetBinContent(i,GJetsHisto.GetBinContent(j)*lumiscale)
        		ZRatios.SetBinContent(i,GJetsRatioHisto.GetBinContent(j)*GJetsPurHisto.GetBinContent(j)*GJetsRatioCorrHisto.GetBinContent(j))
			PurErrNew.SetBinContent(i,1.0+PurErr.GetBinContent(j))
			ZgammaErrUpNew.SetBinContent(i,1.0+ZgammaErrUp.GetBinContent(j))
			ZgammaErrDnNew.SetBinContent(i,1.0-ZgammaErrDn.GetBinContent(j))
			DRErrUpNew.SetBinContent(i,1.0+DRErrUp.GetBinContent(j))
			DRErrDnNew.SetBinContent(i,1.0-DRErrDn.GetBinContent(j))
		if parsenew[1]=="NJets1" and parsenew2[0]=="NJets0" and parsenew[2]==parsenew2[2] and parsenew[3]==parsenew2[3]:
			GJetsHistoNew.SetBinContent(i,GJetsHisto.GetBinContent(j)*lumiscale)
        		ZRatios.SetBinContent(i,GJetsRatioHisto.GetBinContent(j)*GJetsPurHisto.GetBinContent(j)*GJetsRatioCorrHisto.GetBinContent(j))
			PurErrNew.SetBinContent(i,1.0+PurErr.GetBinContent(j))
			ZgammaErrUpNew.SetBinContent(i,1.0+ZgammaErrUp.GetBinContent(j))
			ZgammaErrDnNew.SetBinContent(i,1.0-ZgammaErrDn.GetBinContent(j))
			DRErrUpNew.SetBinContent(i,1.0+DRErrUp.GetBinContent(j))
			DRErrDnNew.SetBinContent(i,1.0-DRErrDn.GetBinContent(j))
	
		if parsenew[1]=="NJets2" and parsenew2[0]=="NJets1" and parsenew[2]==parsenew2[2] and parsenew[3]==parsenew2[3]:
			GJetsHistoNew.SetBinContent(i,GJetsHisto.GetBinContent(j)*lumiscale)
        		ZRatios.SetBinContent(i,GJetsRatioHisto.GetBinContent(j)*GJetsPurHisto.GetBinContent(j)*GJetsRatioCorrHisto.GetBinContent(j))
			PurErrNew.SetBinContent(i,1.0+PurErr.GetBinContent(j))
			ZgammaErrUpNew.SetBinContent(i,1.0+ZgammaErrUp.GetBinContent(j))
			ZgammaErrDnNew.SetBinContent(i,1.0-ZgammaErrDn.GetBinContent(j))
			DRErrUpNew.SetBinContent(i,1.0+DRErrUp.GetBinContent(j))
			DRErrDnNew.SetBinContent(i,1.0-DRErrDn.GetBinContent(j))
	
		if parsenew[1]=="NJets3" and parsenew2[0]=="NJets2" and parsenew[2]==parsenew2[2] and parsenew[3]==parsenew2[3]:
			GJetsHistoNew.SetBinContent(i,GJetsHisto.GetBinContent(j)*lumiscale)
        		ZRatios.SetBinContent(i,GJetsRatioHisto.GetBinContent(j)*GJetsPurHisto.GetBinContent(j)*GJetsRatioCorrHisto.GetBinContent(j))
			PurErrNew.SetBinContent(i,1.0+PurErr.GetBinContent(j))
			ZgammaErrUpNew.SetBinContent(i,1.0+ZgammaErrUp.GetBinContent(j))
			ZgammaErrDnNew.SetBinContent(i,1.0-ZgammaErrDn.GetBinContent(j))
			DRErrUpNew.SetBinContent(i,1.0+DRErrUp.GetBinContent(j))
			DRErrDnNew.SetBinContent(i,1.0-DRErrDn.GetBinContent(j))

		if parsenew[1]=="NJets4" and parsenew2[0]=="NJets3" and parsenew[2]==parsenew2[2] and parsenew[3]==parsenew2[3]:
			GJetsHistoNew.SetBinContent(i,GJetsHisto.GetBinContent(j)*lumiscale)
        		ZRatios.SetBinContent(i,GJetsRatioHisto.GetBinContent(j)*GJetsPurHisto.GetBinContent(j)*GJetsRatioCorrHisto.GetBinContent(j))
			PurErrNew.SetBinContent(i,1.0+PurErr.GetBinContent(j))
			ZgammaErrUpNew.SetBinContent(i,1.0+ZgammaErrUp.GetBinContent(j))
			ZgammaErrDnNew.SetBinContent(i,1.0-ZgammaErrDn.GetBinContent(j))
			DRErrUpNew.SetBinContent(i,1.0+DRErrUp.GetBinContent(j))
			DRErrDnNew.SetBinContent(i,1.0-DRErrDn.GetBinContent(j))

for i in range(1,175):
	inputlabel=ZRatios.GetXaxis().GetBinLabel(i)
        parsenew=inputlabel.split('_')
        for j in range(1,160):
                inputlabel2=DY0btoNb.GetXaxis().GetBinLabel(j)
		parsenew2=inputlabel2.split('-')
		if parsenew[1]=="NJets0" and parsenew2[0]=="NJets0" and parsenew[2]==parsenew2[1] and parsenew[3]==parsenew2[2] and parsenew[4]==parsenew2[3]:
			ZRatios.SetBinContent(i,ZRatios.GetBinContent(i)*DY0btoNb.GetBinContent(j))
			DYStatNew.SetBinContent(i,DYStat.GetBinContent(j))
			DYMCStatNew.SetBinContent(i,DYMCStat.GetBinContent(j))
			DYPurNew.SetBinContent(i,DYPur.GetBinContent(j))
			DYKinNew.SetBinContent(i,DYKin.GetBinContent(j))
			hDYsysNjUpNew.SetBinContent(i, hDYsysNjUp.GetBinContent(j))
			hDYsysNjLowNew.SetBinContent(i,hDYsysNjLow.GetBinContent(j))

		if parsenew[1]=="NJets1" and parsenew2[0]=="NJets0" and parsenew[2]==parsenew2[1] and parsenew[3]==parsenew2[2] and parsenew[4]==parsenew2[3]:
			ZRatios.SetBinContent(i,ZRatios.GetBinContent(i)*DY0btoNb.GetBinContent(j))
			DYStatNew.SetBinContent(i,DYStat.GetBinContent(j))
			DYMCStatNew.SetBinContent(i,DYMCStat.GetBinContent(j))
			DYPurNew.SetBinContent(i,DYPur.GetBinContent(j))
			DYKinNew.SetBinContent(i,DYKin.GetBinContent(j))
			hDYsysNjUpNew.SetBinContent(i, hDYsysNjUp.GetBinContent(j))
			hDYsysNjLowNew.SetBinContent(i,hDYsysNjLow.GetBinContent(j))

		if parsenew[1]=="NJets2" and parsenew2[0]=="NJets1" and parsenew[2]==parsenew2[1] and parsenew[3]==parsenew2[2] and parsenew[4]==parsenew2[3]:
			ZRatios.SetBinContent(i,ZRatios.GetBinContent(i)*DY0btoNb.GetBinContent(j))
			DYStatNew.SetBinContent(i,DYStat.GetBinContent(j))
			DYMCStatNew.SetBinContent(i,DYMCStat.GetBinContent(j))
			DYPurNew.SetBinContent(i,DYPur.GetBinContent(j))
			DYKinNew.SetBinContent(i,DYKin.GetBinContent(j))
			hDYsysNjUpNew.SetBinContent(i, hDYsysNjUp.GetBinContent(j))
			hDYsysNjLowNew.SetBinContent(i,hDYsysNjLow.GetBinContent(j))

		if parsenew[1]=="NJets3" and parsenew2[0]=="NJets2" and parsenew[2]==parsenew2[1] and parsenew[3]==parsenew2[2] and parsenew[4]==parsenew2[3]:
			ZRatios.SetBinContent(i,ZRatios.GetBinContent(i)*DY0btoNb.GetBinContent(j))
			DYStatNew.SetBinContent(i,DYStat.GetBinContent(j))
			DYMCStatNew.SetBinContent(i,DYMCStat.GetBinContent(j))
			DYPurNew.SetBinContent(i,DYPur.GetBinContent(j))
			DYKinNew.SetBinContent(i,DYKin.GetBinContent(j))
			hDYsysNjUpNew.SetBinContent(i, hDYsysNjUp.GetBinContent(j))
			hDYsysNjLowNew.SetBinContent(i,hDYsysNjLow.GetBinContent(j))

		if parsenew[1]=="NJets4" and parsenew2[0]=="NJets3" and parsenew[2]==parsenew2[1] and parsenew[3]==parsenew2[2] and parsenew[4]==parsenew2[3]:
			ZRatios.SetBinContent(i,ZRatios.GetBinContent(i)*DY0btoNb.GetBinContent(j))
			DYStatNew.SetBinContent(i,DYStat.GetBinContent(j))
			DYMCStatNew.SetBinContent(i,DYMCStat.GetBinContent(j))
			DYPurNew.SetBinContent(i,DYPur.GetBinContent(j))
			DYKinNew.SetBinContent(i,DYKin.GetBinContent(j))
			hDYsysNjUpNew.SetBinContent(i, hDYsysNjUp.GetBinContent(j))
			hDYsysNjLowNew.SetBinContent(i,hDYsysNjLow.GetBinContent(j))

	binlabel="GJetObsStatErr"+"_"+parsenew[1]+"_"+parsenew[3]+"_"+parsenew[4]
	ZRatios.GetXaxis().SetBinLabel(i,binlabel)
for i in range(1,175):
	if GJetsHistoNew.GetBinContent(i)>0.0:ZPredNew.SetBinContent(i,GJetsHistoNew.GetBinContent(i)*ZRatios.GetBinContent(i))
	else: ZPredNew.SetBinContent(i,ZRatios.GetBinContent(i))
'''
fout= TFile("HadTauEstimation_data.root", "RECREATE")
fout.cd();
hadtauSearchBin.Write("searchBin_nominal")
hadtauClosure.Write("searchBin_closureUncertainty")
hadtauClosureCorr.Write("searchBin_closureUncertainty_adhoc")
hadtauTrigSys.Write("searchBin_TrigEffUncertainty")
hadtauDiLep.Write("searchBin_DileptonUncertainty")
hadtauMuFromTau.Write("searchBin_MuFromTauStat")
hadtauBmistagUp.Write("searchBin_BMistagUp")
hadtauBmistagDn.Write("searchBin_BMistagDn")
hadtauJECUp.Write("searchBin_JECSysUp")
hadtauJECDn.Write("searchBin_JECSysDn")
hadtauMuRecoUp.Write("searchBin_MuRecoSysUp")
hadtauMuRecoDn.Write("searchBin_MuRecoSysDn")
hadtauMuIsoUp.Write("searchBin_MuIsoSysUp")
hadtauMuIsoDn.Write("searchBin_MuIsoSysDn")
hadtauMuRecoIsoUp.Write("searchBin_MuRecoIsoUp");
hadtauMuRecoIsoDn.Write("searchBin_MuRecoIsoDn");
hadtauMTUp.Write("searchBin_MTSysUp")
hadtauMTDn.Write("searchBin_MTSysDn")
hadtauTkIsoEffStat.Write("searchBin_IsoTrkVetoEffUncertaintyStat")
hadtauTkIsoEffSys.Write("searchBin_IsoTrkVetoEffUncertaintySys")
hadtauMTEffStat.Write("searchBin_MtEffStat")
hadtauAccStat.Write("searchBin_AccStat")
hadtauPDFUp.Write("searchBin_AccSysPDFUp")
hadtauPDFDn.Write("searchBin_AccSysPDFDn")
hadtauPDFScaleUp.Write("searchBin_AccSysScaleUp")
hadtauPDFScaleDn.Write("searchBin_AccSysScaleDn")
hadtauStatUnc.Write("searchBin_StatUncertainties")
#ZPredNew.Write("ZPred")
#ZRatios.Write("ZRatios")
#GJetsHistoNew.Write("GammaObs");
fout.Close()	
