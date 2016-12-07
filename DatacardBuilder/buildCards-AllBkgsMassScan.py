from ROOT import *
import os
import math
import sys
from searchRegion import *
from singleBin import *
from cardUtilities import *
import random
from optparse import OptionParser
from GenMHTCorrection import *
parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option("--signal", dest="signal", default = 'SMSqqqq1000',help="mass of LSP", metavar="signal")
parser.add_option("--tag", dest="tag", default = 'SinglePhoton1',help="mass of LSP", metavar="tag")
parser.add_option("--mu", dest="mu", default = 1.,help="mass of LSP", metavar="mu")
parser.add_option("--lumi", dest="lumi", default = 10.,help="mass of LSP", metavar="lumi")
parser.add_option('--fastsim', action='store_true', dest='fastsim', default=False, help='no X11 windows')
parser.add_option('--realData', action='store_true', dest='realData', default=False, help='no X11 windows')

parser.add_option('--qcdOnly', action='store_true', dest='qcdOnly', default=False, help='no X11 windows')
parser.add_option('--zvvOnly', action='store_true', dest='zvvOnly', default=False, help='no X11 windows')
parser.add_option('--tauOnly', action='store_true', dest='tauOnly', default=False, help='no X11 windows')
parser.add_option('--llpOnly', action='store_true', dest='llpOnly', default=False, help='no X11 windows')
parser.add_option('--allBkgs', action='store_true', dest='allBkgs', default=False, help='no X11 windows')
parser.add_option("--mGo", dest="mGo", default='1000', help="Mass of Gluino", metavar="mGo")
parser.add_option("--mLSP", dest="mLSP", default='900', help="Mass of LSP", metavar="mLSP")
(options, args) = parser.parse_args()


#########################################################################################################
## to do:
## .......
#########################################################################################################


if __name__ == '__main__':

	sms = "SMS"+options.signal[2:]+options.mGo;
	if options.fastsim: sms = options.signal+'_'+options.mGo+'_'+options.mLSP;
	tag = options.tag;
	lumi = float(options.lumi);
	signalmu = float(options.mu);
	odir = 'testCards-%s-%s-%1.1f-mu%0.1f/' % ( tag,sms, lumi, signalmu );
	idir = 'inputHistograms/histograms_%1.1ffb/' % ( ((lumi)) );
	if os.path.exists(odir): os.system( "rm -rf %s" % (odir) );
	os.makedirs(odir);

	print odir, signalmu

	######################################################################
	######################################################################
	## 1. Get the input histograms from each of the background teams
	######################################################################
	######################################################################

	# --------------------------------------------
	# signal 
	signaldirtag = idir;
	if options.fastsim: 
		#signaldirtag += "/fastsimSignalScan";
		if "T2bb" in sms:  signaldirtag ="inputHistograms/fastsimSignalT2bb"
		if "T1tttt" in sms:  signaldirtag ="inputHistograms/fastsimSignalT1tttt"
		if "T1bbbb" in sms:  signaldirtag ="inputHistograms/fastsimSignalT1bbbb"
		if "T1qqqq" in sms:  signaldirtag ="inputHistograms/fastsimSignalT1qqqq"
		if "T5qqqqVV" in sms:  signaldirtag ="inputHistograms/fastsimSignalT5qqqqVV"
		#if ("T1" in sms or "T5qqqqVV" in sms): signaldirtag +="Gluino"
		if ("T2qq" in sms): signaldirtag ="inputHistograms/fastsimSignalT2qq"
		if ("T2tt" in sms): signaldirtag ="inputHistograms/fastsimSignalT2tt"
		if "T1ttbb" in sms or "T1tbtb" in sms: signaldirtag="/fastsimSignalScanMixedFinalState"
	else: signaldirtag ="inputHistograms/FullSim"
	signaltag = "RA2bin_"+sms;
	parse=sms.split('_')
	model=parse[0]
	#print parse
	if options.fastsim: signaltag+="_fast"
	CorrSigHist=genMHTCorr(signaldirtag,signaltag,lumi)
	MHTSyst=genMHTSyst(signaldirtag,signaltag,lumi)	
	tagsForSignalRegion = binLabelsToList(CorrSigHist);	
	LL_file=TFile(idir+"LLPrediction_combined.root");
	#LL_file = TFile(idir+"/LLPrediction.root");
	LLPrediction_Hist=LL_file.Get("Prediction_data/totalPred_LL")		
	#totalCS_LL=LL_file.Get("totalCS_LL")
	LLAvgHeight_Hist=LL_file.Get("Prediction_data/avgWeight_0L1L")
	LLControlStatUnc_Hist=LL_file.Get("Prediction_data/totalPredControlStat_LL")	
	HadTau_file = TFile(idir+"/HadTauEstimation_data.root");
	HadTauPrediction=HadTau_file.Get("searchBin_nominal");
	HadTauStatUnc=HadTauPrediction.Clone("HadTauStatUnc")
	for i in range(1,175):
		if HadTauPrediction.GetBinContent(i)>0.0:HadTauStatUnc.SetBinContent(1, 1.0+HadTauStatUnc.GetBinError(i)/HadTauPrediction.GetBinContent(i))
	
	#HERE ADD Bin Errors for the Had Tau Stat Error
	DYinputfile = TFile(idir+"/ZinvHistos.root")
	ZPred=DYinputfile.Get("ZinvBGpred")
	ZRatios=DYinputfile.Get("hzvvTF")
	GammaObs=DYinputfile.Get("hzvvgJNobs")
	#ZgammaErrUp=DYinputfile.Get("hzvvZgRerrUp");
	#ZgammaErrDn=DYinputfile.Get("hzvvZgRerrLow");
	GammaETErr=DYinputfile.Get("hzvvgJEtrgErr")
	FdirErr=DYinputfile.Get("hzvvgJFdirErr")
	GammaPurityErr=DYinputfile.Get("hzvvgJPurErr");
	DoubleRatioErrUp=DYinputfile.Get("hzvvZgDRerrUp");
	DoubleRatioErrDn=DYinputfile.Get("hzvvZgDRerrLow");
	ZScaleErr=DYinputfile.Get("hzvvScaleErr");
	DYStatErr=DYinputfile.Get("hzvvDYstat");
	DYPurErr=DYinputfile.Get("hzvvDYsysPur");
	DYKinErr=DYinputfile.Get("hzvvDYsysKin");
	DYMCStatErr=DYinputfile.Get("hzvvDYMCstat");
	DYNJExtrapErrUp=DYinputfile.Get("hzvvDYsysNjUp");
	DYNJExtrapErrDn=DYinputfile.Get("hzvvDYsysNjLow");
	for i in range(1,DYNJExtrapErrDn.GetNbinsX()+1):	
		#ZgammaErrDn.SetBinContent(i,1.0/ZgammaErrDn.GetBinContent(i))
		DYNJExtrapErrDn.SetBinContent(i,1.0/DYNJExtrapErrDn.GetBinContent(i))
		DoubleRatioErrDn.SetBinContent(i,1.0/DoubleRatioErrDn.GetBinContent(i))
	for i in range(1, HadTauPrediction.GetNbinsX()+1):
		if HadTauPrediction.GetBinContent(i)>0.0: HadTauStatUnc.SetBinContent(i,1.0+HadTauPrediction.GetBinError(i)/HadTauPrediction.GetBinContent(i));
		else:HadTauStatUnc.SetBinContent(i,1.0+HadTauPrediction.GetBinError(i))
	# QCD, low delta phi
	ratesForSignalRegion_QCDList = [];
	NSRForSignalRegion_QCDList = textToList(idir+"/qcd-bg-combine-input.txt",6);
	ratesForLowdphiRegion_QCDList = [];
	NCRForLowdphiRegion_QCDList = textToList(idir+"/qcd-bg-combine-input.txt",2);
	obsForLowdphiRegion_QCDList = [];
	ratiosForLowdphiRegion = textToList(idir+"/qcd-bg-combine-input.txt",5);
	ContaminForLowdphiRegion = textToList(idir+"/qcd-bg-combine-input.txt",3);
	tagsForLowDPhiRegion = tagsForSignalRegion[:]
	QCDcontributionsPerBin = [];
	for i in range(len(tagsForLowDPhiRegion)): 
		#NOTE TEMPORARY!!!!!!!!
		QCDcontributionsPerBin.append( [ 'sig','qcd','contam' ] );
		#ContaminForLowdphiRegion[i]=0
		ContaminSubtracted=NCRForLowdphiRegion_QCDList[i]-ContaminForLowdphiRegion[i]
		if(ContaminSubtracted>0.0 and NSRForSignalRegion_QCDList[i]>0.0): 
			ratesForLowdphiRegion_QCDList.append(ContaminSubtracted)
			ratesForSignalRegion_QCDList.append(NSRForSignalRegion_QCDList[i]*12.9/lumi)	
		else:
			ratesForLowdphiRegion_QCDList.append(1.0)
			ratesForSignalRegion_QCDList.append(ratiosForLowdphiRegion[i]);
			NSRForSignalRegion_QCDList[i]=0.0
		if NSRForSignalRegion_QCDList[i]<=0.0:NSRForSignalRegion_QCDList[i]=0.0 #protection against -0.00 issue
		obsForLowdphiRegion_QCDList.append( NCRForLowdphiRegion_QCDList[i]);
	LowdphiControlRegion = searchRegion('Lowdphi', QCDcontributionsPerBin, tagsForLowDPhiRegion);	
	qcdcontrolRegion_Rates = [];
	qcdcontrollRegion_Observed = [];
	for i in range(LowdphiControlRegion._nBins):
		curobsC = 0;
		curobsC += obsForLowdphiRegion_QCDList[i]
		currateC = [];
		currateC.append( 0. );
		currateC.append( ratesForLowdphiRegion_QCDList[i] );
		if(NCRForLowdphiRegion_QCDList[i]>0.5) :currateC.append(ContaminForLowdphiRegion[i]);	
		else: currateC.append(0.0)
		qcdcontrolRegion_Rates.append(currateC);
		qcdcontrollRegion_Observed.append(curobsC);	
	LowdphiControlRegion.fillRates(qcdcontrolRegion_Rates);
	LowdphiControlRegion.setObservedManually(qcdcontrollRegion_Observed);
	LowdphiControlRegion.writeRates();

	contributionsPerBin = [];
	f = TFile(odir+'yields.root', 'recreate')
	data = TH1F( 'data', 'data', 174, 0, 174 )
	qcd = TH1F( 'QCD', 'QCD', 174, 0, 174 )
	zvv = TH1F( 'Zvv', 'Zvv', 174, 0, 174 )
	ll = TH1F( 'LL', 'LL', 174, 0, 174 )
	tau = TH1F( 'tau', 'tau', 174, 0, 174 )
	sig = TH1F( 'sig', 'sig', 174, 0, 174 )
	for i in range(len(tagsForSignalRegion)): 	
		tmpcontributions = [];
		tmpcontributions.append('sig');
		tmpcontributions.append('WTopSL');
		tmpcontributions.append('WTopSLHighW');
		tmpcontributions.append('WTopHad');
		tmpcontributions.append('WTopHadHighW');
		tmpcontributions.append('zvv')
		tmpcontributions.append('qcd')
		contributionsPerBin.append(tmpcontributions)
	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)
	signalRegion_Rates = [];
	signalRegion_Obs = [];
	DataHist_In=TFile("inputHistograms/histograms_%1.1ffb/RA2bin_signalICHEP.root" %lumi)
	Data_Hist=DataHist_In.Get("RA2bin_data")
	Data_List=binsToList(Data_Hist)
	for i in range(signalRegion._nBins):
		tmpList = [];
		srobs = 0;
		tmpList.append(CorrSigHist.GetBinContent(i+1)*12.9/lumi)
		tmpList.append(LLPrediction_Hist.GetBinContent(i+1)*12.9/lumi)
		tmpList.append(LLAvgHeight_Hist.GetBinContent(i+1))
		tmpList.append(HadTauPrediction.GetBinContent(i+1)*12.9/lumi)
		tmpList.append(0.25)
		if GammaObs.GetBinContent(i+1)>0.0:tmpList.append(ZPred.GetBinContent(i+1)*12.9/lumi)
		else: tmpList.append(ZRatios.GetBinContent(i+1))
		tmpList.append( ratesForSignalRegion_QCDList[i] );
		#srobs=(ZPred.GetBinContent(i+1)+LLPrediction_Hist.GetBinContent(i+1)+HadTauPrediction.GetBinContent(i+1)+(NSRForSignalRegion_QCDList[i]))
		#if (int(options.mGo)==1400 and int(options.mLSP)==600):
			#srobs=srobs+CorrSigHist.GetBinContent(i+1);
		srobs=Data_List[i]
		qcd.Fill(i+.5, NSRForSignalRegion_QCDList[i]*12.9/lumi)
		zvv.Fill(i+.5, ZPred.GetBinContent(i+1)*12.9/lumi)
		ll.Fill(i+.5, + LLPrediction_Hist.GetBinContent(i+1)*12.9/lumi)
		tau.Fill(i+.5, HadTauPrediction.GetBinContent(i+1)*12.9/lumi)	
		sig.Fill(i+.5,CorrSigHist.GetBinContent(i+1)*signalmu*12.9/lumi)
		#randPois=TRandom3(random.randint(1,10000000))
		#srobs=randPois.Poisson(srobs)
		
		signalRegion_Rates.append(tmpList)
		signalRegion_Obs.append(srobs)
		data.Fill(i+.5, srobs)

	signalRegion.fillRates(signalRegion_Rates );
	signalRegion.setObservedManually(signalRegion_Obs)
	signalRegion.writeRates();
        f.Write()
	f.Close()
	########################

	#Signal Systematics
	
	#######################

	signalSysSFUp_file=TFile(signaldirtag+"/RA2bin_signal_btagSFuncUpFormat.root");
	signalSysSFDown_file=TFile(signaldirtag+"/RA2bin_signal_btagSFuncDownFormat.root");
	signalSysMisSFUp_file=TFile(signaldirtag+"/RA2bin_signal_mistagSFuncUpFormat.root");
	signalSysMisSFDown_file=TFile(signaldirtag+"/RA2bin_signal_mistagSFuncDownFormat.root");
	signalSysTrigSystUp_file=TFile(signaldirtag+"/RA2bin_signal_trigSystUncUpFormat.root");
	signalSysTrigSystDown_file=TFile(signaldirtag+"/RA2bin_signal_trigSystUncDownFormat.root");
	signalSysTrigStatUp_file=TFile(signaldirtag+"/RA2bin_signal_trigStatUncUpFormat.root");
	signalSysTrigStatDown_file=TFile(signaldirtag+"/RA2bin_signal_trigStatUncDownFormat.root");
	signalSysJERUp_file        =TFile(signaldirtag+"/RA2bin_signal_JERupFormat.root");
	signalSysJERDown_file      =TFile(signaldirtag+"/RA2bin_signal_JERdownFormat.root");
	signalSysJECUp_file        =TFile(signaldirtag+"/RA2bin_signal_JECupFormat.root");
	signalSysJECDown_file      =TFile(signaldirtag+"/RA2bin_signal_JECdownFormat.root");
	signalSysScaleUp_file      =TFile(signaldirtag+"/RA2bin_signal_scaleuncUpFormat.root");
	signalSysScaleDown_file    =TFile(signaldirtag+"/RA2bin_signal_scaleuncDownFormat.root");
	#signalSysPUUpFormat_file         =TFile(signaldirtag+"/RA2bin_signal_puuncUpFormat.root");
	#signalSysPUDownFormat_file       =TFile(signaldirtag+"/RA2bin_signal_puuncDownFormat.root");
	#signalSysPDFUpFormat_file         =TFile(signaldirtag+"/RA2bin_signal_pdfuncUpFormat.root");
	#signalSysPDFDownFormat_file       =TFile(signaldirtag+"/RA2bin_signal_pdfuncDownFormat.root");
	signalSysISRUp_file         =TFile(signaldirtag+"/RA2bin_signal_isruncUpFormat.root");
	signalSysISRDown_file       =TFile(signaldirtag+"/RA2bin_signal_isruncDownFormat.root");
	signalMCStatError_file      =TFile(signaldirtag+"/RA2bin_signal_MCStatErr.root");
	if options.fastsim:
		signalSysbtagCFuncUp_file=TFile(signaldirtag+"/RA2bin_signal_btagCFuncUpFormat.root");
		signalSysbtagCFuncDown_file=TFile(signaldirtag+"/RA2bin_signal_btagCFuncDownFormat.root");
		signalSysctagCFuncUp_file=TFile(signaldirtag+"/RA2bin_signal_ctagCFuncUpFormat.root");
		signalSysctagCFuncDown_file=TFile(signaldirtag+"/RA2bin_signal_ctagCFuncDownFormat.root");
		signalSysmistagCFuncUp_file=TFile(signaldirtag+"/RA2bin_signal_mistagCFuncUpFormat.root");
		signalSysmistagCFuncDown_file=TFile(signaldirtag+"/RA2bin_signal_mistagCFuncDownFormat.root");
	#Get Histograms:
	signalSysSFUp=signalSysSFUp_file.Get(signaltag)	
	signalSysSFDown=signalSysSFDown_file.Get(signaltag)		
	signalSysMisSFUp=signalSysMisSFUp_file.Get(signaltag)
	signalSysMisSFDown=signalSysMisSFDown_file.Get(signaltag)
	signalSysTrigSystUp=signalSysTrigSystUp_file.Get(signaltag)
	signalSysTrigSystDown=signalSysTrigSystDown_file.Get(signaltag)
	signalSysTrigStatUp=signalSysTrigStatUp_file.Get(signaltag)
	signalSysTrigStatDown=signalSysTrigStatDown_file.Get(signaltag)
	signalSysJERUp=signalSysJERUp_file.Get(signaltag)
	signalSysJERDown=signalSysJERDown_file.Get(signaltag)
	signalSysJECUp=signalSysJECUp_file.Get(signaltag)
	signalSysJECDown=signalSysJECDown_file.Get(signaltag)

	signalSysScaleUp=signalSysScaleUp_file.Get(signaltag)
	signalSysScaleDown=signalSysScaleDown_file.Get(signaltag)
	signalMCStatError=signalMCStatError_file.Get(signaltag)
	signalSysbtagCFuncUp=signalSysbtagCFuncUp_file.Get(signaltag)
	signalSysbtagCFuncDown=signalSysbtagCFuncDown_file.Get(signaltag)
	signalSysctagCFuncUp=signalSysctagCFuncUp_file.Get(signaltag)
	signalSysctagCFuncDown=signalSysctagCFuncDown_file.Get(signaltag)
	signalSysmistagCFuncUp=signalSysmistagCFuncUp_file.Get(signaltag)
	signalSysmistagCFuncDown=signalSysmistagCFuncDown_file.Get(signaltag)
	
        signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.027);
        signalRegion.addSingleSystematic('EvtFilters','lnN',['sig'],1.03);
        signalRegion.addSingleSystematic('JetIDUnc','lnN',['sig'],1.01);
	signalRegion.addSystematicsLine('lnN',['sig'],signalMCStatError);	
	signalRegion.addSystematicsLine('lnU',['sig'],MHTSyst);
	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysSFUp,signalSysSFDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysMisSFUp,signalSysMisSFDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysTrigSystUp,signalSysTrigSystDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysTrigStatUp,signalSysTrigStatDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysJERUp,signalSysJERDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysJECUp,signalSysJECDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysScaleUp,signalSysScaleDown)
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysbtagCFuncUp,signalSysbtagCFuncDown)		
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysctagCFuncUp,signalSysctagCFuncDown)		
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysmistagCFuncUp,signalSysmistagCFuncDown)		
	##############

	#Correlate HAD TAU AND LOST LEPTON SYSTEMATICS


	############

	signalRegion.addCorrelSystematicLine('lnN', ['WTopSL','WTopHad'],LLControlStatUnc_Hist,HadTauStatUnc)
	CSZero=LLAvgHeight_Hist.Clone()	
	HadTauHighW=LLAvgHeight_Hist.Clone()
	for i in range(1,CSZero.GetNbinsX()+1):
		CSZero.SetBinContent(i,0.0)
		HadTauHighW.SetBinContent(i,0.25)
		LLAvgHeight_Hist.GetXaxis().SetBinLabel(i,"HighWeightStatUnc_"+LLAvgHeight_Hist.GetXaxis().GetBinLabel(i))
	signalRegion.addCorrelGammaSystematic(['WTopSLHighW','WTopHadHighW'],CSZero,LLAvgHeight_Hist,HadTauHighW)
	for i in range(len(GammaObs)):GammaObs[i]=GammaObs[i]*12.9/lumi
	signalRegion.addGammaSystematic(['zvv'],GammaObs,ZRatios )
	#signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],ZgammaErrUp,ZgammaErrDn)
	signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],DoubleRatioErrUp,DoubleRatioErrDn)
	signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],DYNJExtrapErrUp,DYNJExtrapErrDn)
	signalRegion.addSystematicsLine('lnN',['zvv'],ZScaleErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],GammaPurityErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],DYStatErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],DYPurErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],DYKinErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],DYMCStatErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],GammaETErr)
	signalRegion.addSystematicsLine('lnN',['zvv'],FdirErr)
	HadTauClosureUnc=HadTau_file.Get("totalPredNonClosure_HadTau")		
	HadTauClosureCorrUnc=HadTau_file.Get("totalPredAdhoc_HadTau")		
	HadTauBMistagUp=HadTau_file.Get("totalPredBMistagUp_HadTau")
	HadTauBMistagDn=HadTau_file.Get("totalPredBMistagDown_HadTau")
	HadTauJECUp=HadTau_file.Get("searchBin_JECSysUp")
	HadTauJECDn=HadTau_file.Get("searchBin_JECSysDn")
	HadTauDiMuonUnc=HadTau_file.Get("totalPredDilep_HadTau")
	HadTauMuFromTau=HadTau_file.Get("totalPredMuFromTauStat_HadTau")

	HadTauTrigEff=HadTau_file.Get("totalPredTrigSyst_HadTau")
	signalRegion.addSystematicsLine('lnN',['WTopHad'],HadTauClosureUnc)
	signalRegion.addSystematicsLine('lnN',['WTopHad'],HadTauClosureCorrUnc)
	signalRegion.addSystematicsLineAsymShape('lnN',['WTopHad'],HadTauBMistagUp,HadTauBMistagDn)
	signalRegion.addSystematicsLineAsymShape('lnN',['WTopHad'],HadTauJECUp,HadTauJECDn)
	signalRegion.addSystematicsLine('lnN',['WTopHad'],HadTauDiMuonUnc)	
	signalRegion.addSystematicsLine('lnN',['WTopHad'],HadTauMuFromTau)	
	signalRegion.addSystematicsLine('lnN',['WTopHad'],HadTauTrigEff)	
	HadTauMTSysUp=HadTau_file.Get("totalPredMTSysUp_HadTau")	
	HadTauMTSysDn=HadTau_file.Get("totalPredMTSysDown_HadTau")	
	LLSysMTUp=LL_file.Get("Prediction_data/totalPredMTWSysUp_LL")	
	LLSysMTDn=LL_file.Get("Prediction_data/totalPredMTWSysDown_LL")	
	signalRegion.addCorrelAsymSystematicLine('lnN', ['WTopSL','WTopHad'],LLSysMTUp,LLSysMTDn,HadTauMTSysUp,HadTauMTSysDn)	
	HadTauMTEffStat=HadTau_file.Get("totalPredMtEffStat_HadTau")	
	LLStatMTStatUp=LL_file.Get("Prediction_data/totalPredMTWStatUp_LL")	
	LLStatMTStatDn=LL_file.Get("Prediction_data/totalPredMTWStatDown_LL")	
	HadTauMTEffStatDn=HadTauMTEffStat.Clone("HadTauMTEffStatDn")
	for i in range(1,175):HadTauMTEffStatDn.SetBinContent(i,1.0/HadTauMTEffStat.GetBinContent(i))
	signalRegion.addCorrelAsymSystematicLine('lnN', ['WTopSL','WTopHad'],LLStatMTStatUp,LLStatMTStatDn,HadTauMTEffStat,HadTauMTEffStatDn)	

	HadTauAccStat=HadTau_file.Get("totalPredLepAccStat_LL")
	LLAccStatUp=LL_file.Get("Prediction_data/totalPredLepAccStatUp_LL")
	LLAccStatDn=LL_file.Get("Prediction_data/totalPredLepAccStatDown_LL")
	HadTauAccStatDn=HadTauAccStat.Clone("HadTauAccStatDn")
        for i in range(1,175):HadTauAccStatDn.SetBinContent(i,1.0/HadTauAccStatDn.GetBinContent(i))
	signalRegion.addCorrelAsymSystematicLine('lnN', ['WTopSL','WTopHad'],LLAccStatUp,LLAccStatDn,HadTauAccStat,LLAccStatDn)

	HadTauAccPDFSysUp=HadTau_file.Get("totalPredPDFUp_LL")
	HadTauAccPDFSysDn=HadTau_file.Get("totalPredPDFDown_LL")
	LLAccPDFSysUp=LL_file.Get("Prediction_data/totalPredLepAccSysUp_LL")
	LLAccPDFSysDn=LL_file.Get("Prediction_data/totalPredLepAccSysDown_LL")
	signalRegion.addCorrelAsymSystematicLine('lnN',['WTopSL','WTopHad'],HadTauAccPDFSysUp,HadTauAccPDFSysDn, HadTauAccPDFSysUp,HadTauAccPDFSysDn)

	HadTauAccQScaleUp=HadTau_file.Get("totalPredScaleUp_LL");
	HadTauAccQScaleDn=HadTau_file.Get("totalPredScaleDown_LL");
	LLQScaleSysUp=LL_file.Get("Prediction_data/totalPredLepAccQsquareSysUp_LL")
	LLQScaleSysDn=LL_file.Get("Prediction_data/totalPredLepAccQsquareSysDown_LL")
	signalRegion.addCorrelAsymSystematicLine('lnN',['WTopSL','WTopHad'],LLQScaleSysUp,LLQScaleSysDn, HadTauAccQScaleUp,HadTauAccQScaleDn)

	LLIsoTrackStatUp=LL_file.Get("Prediction_data/totalPredIsoTrackStatUp_LL")
	LLIsoTrackStatDn=LL_file.Get("Prediction_data/totalPredIsoTrackStatDown_LL")
	HadTauIsoTrackStat=HadTau_file.Get("totalPredIsoTrackStat_LL")	
	HadTauIsoTrackStatDn=HadTauIsoTrackStat.Clone("HadTauIsoTrackStatDn")
	for i in range(1,175):HadTauIsoTrackStatDn.SetBinContent(i,1.0/HadTauIsoTrackStat.GetBinContent(i))
        signalRegion.addCorrelAsymSystematicLine('lnN',['WTopSL','WTopHad'],LLIsoTrackStatUp,LLIsoTrackStatDn, HadTauIsoTrackStat,HadTauIsoTrackStatDn)

	HadTauIsoTrackSys=HadTau_file.Get("totalPredIsoTrackSys_LL")
	LLIsoTrackSysUp=LL_file.Get("Prediction_data/totalPredIsoTrackSysUp_LL")
	LLIsoTrackSysDn=LL_file.Get("Prediction_data/totalPredIsoTrackSysDown_LL")
        HadTauIsoTrackSysDn=HadTauIsoTrackSys.Clone("HadTauIsoTrackSysDn")
        for i in range(1,175):HadTauIsoTrackSysDn.SetBinContent(i,1.0/HadTauIsoTrackSys.GetBinContent(i))
        signalRegion.addCorrelAsymSystematicLine('lnN',['WTopSL','WTopHad'],LLIsoTrackSysUp,LLIsoTrackSysDn, HadTauIsoTrackSys,HadTauIsoTrackSysDn)
	LLSysIsoUp=LL_file.Get("Prediction_data/totalPredMuIsoSysUp_LL")	
	LLSysIsoDn=LL_file.Get("Prediction_data/totalPredMuIsoSysDown_LL")	
	HadTauMuIsoUp=HadTau_file.Get("totalPredMuIsoSysUp_LL")
	HadTauMuIsoDn=HadTau_file.Get("totalPredMuIsoSysDown_LL")
	signalRegion.addCorrelAsymSystematicLine('lnN',['WTopSL','WTopHad'],LLSysIsoUp,LLSysIsoDn,HadTauMuIsoUp,HadTauMuIsoDn)
	LLSysRecoUp=LL_file.Get("Prediction_data/totalPredMuRecoSysUp_LL")	
	LLSysRecoDn=LL_file.Get("Prediction_data/totalPredMuRecoSysDown_LL")	
	HadTauMuRecoUp=HadTau_file.Get("totalPredMuRecoSysUp_LL")
	HadTauMuRecoDn=HadTau_file.Get("totalPredMuRecoSysDown_LL")
	signalRegion.addCorrelAsymSystematicLine('lnN',['WTopSL','WTopHad'],LLSysRecoUp,LLSysRecoDn,HadTauMuRecoUp,HadTauMuRecoDn)
	PredDir=LL_file.Get("Prediction_data")	
	names = [k.GetName() for k in PredDir.GetListOfKeys()]
	for n in names:
		if "totalPred_LL" in n:continue;
		if "totalCS_LL" in n:continue;
		if "nEvtsCS_LL" in n:continue;
		if "avgWeight_0L1L" in n:continue
		if "totalPredControlStat_LL" in n:continue
		if "Up" in n:
			#Asymetric Uncertainty:
			UpErr=LL_file.Get("Prediction_data/%s" %(n))
			ndown=n.replace("Up","Down")
			DnErr=LL_file.Get("Prediction_data/%s" %(ndown))
			if "totalPredNonClosure" in n or "Elec" in n or "DiLepContribution" in n : 
				signalRegion.addSystematicsLineAsymShape('lnN',['WTopSL'],UpErr,DnErr)
	### QCD uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.qcdOnly:	
		ListOfQCDSysK1 = textToListStr(idir+"/qcd-bg-combine-input.txt",7)
		ListOfQCDSysK2 = textToListStr(idir+"/qcd-bg-combine-input.txt",8)
		ListOfQCDSysK3 = textToListStr(idir+"/qcd-bg-combine-input.txt",9)
		ListOfQCDSysK4 = textToListStr(idir+"/qcd-bg-combine-input.txt",10)
		ListOfQCDSysK5 = textToListStr(idir+"/qcd-bg-combine-input.txt",11)
		ListOfQCDSysK6 = textToListStr(idir+"/qcd-bg-combine-input.txt",12)
		ListOfQCDSysK7 = textToListStr(idir+"/qcd-bg-combine-input.txt",13)
		ListOfQCDSysK8 = textToListStr(idir+"/qcd-bg-combine-input.txt",14)	
		ListOfQCDSysK9 = textToListStr(idir+"/qcd-bg-combine-input.txt",15)
		ListOfQCDSysK10 = textToListStr(idir+"/qcd-bg-combine-input.txt",16)
		ListOfQCDSysK11 = textToListStr(idir+"/qcd-bg-combine-input.txt",17)
		ListOfQCDSysK12 = textToListStr(idir+"/qcd-bg-combine-input.txt",18)
		ListOfQCDSysK13 = textToListStr(idir+"/qcd-bg-combine-input.txt",19)	
		ListOfQCDSysK14 = textToListStr(idir+"/qcd-bg-combine-input.txt",20)	
		ListOfQCDSysK15 = textToListStr(idir+"/qcd-bg-combine-input.txt",21)	
		ListOfQCDSysK16 = textToListStr(idir+"/qcd-bg-combine-input.txt",22)	
		ListOfQCDSysK17 = textToListStr(idir+"/qcd-bg-combine-input.txt",23)	
		ListOfQCDSysK18 = textToListStr(idir+"/qcd-bg-combine-input.txt",24)	
		ListOfQCDSysK19 = textToListStr(idir+"/qcd-bg-combine-input.txt",25)	
		ListOfQCDSysK20 = textToListStr(idir+"/qcd-bg-combine-input.txt",26)	
		ListOfQCDSysK21 = textToListStr(idir+"/qcd-bg-combine-input.txt",27)	
		ListOfQCDSysK22 = textToListStr(idir+"/qcd-bg-combine-input.txt",28)	
		ListOfQCDSysK23 = textToListStr(idir+"/qcd-bg-combine-input.txt",29)	
		ListOfMCCSys = textToListStr(idir+"/qcd-bg-combine-input.txt",30)	
		#print ListOfMCCSys
		ContaminUncForLowdphiRegion = textToList(idir+"/qcd-bg-combine-input.txt",4);

		for i in range(len(tagsForSignalRegion)):
			parse=tagsForSignalRegion[i].split("_")
			signalRegion.addSingleSystematic("QCDControlC"+tagsForSignalRegion[i],'lnU','qcd',100,'',i);
			LowdphiControlRegion.addSingleSystematic("QCDControlC"+tagsForSignalRegion[i],'lnU','qcd',100,'',i);				
			if(ContaminForLowdphiRegion[i]>0.0 and (NCRForLowdphiRegion_QCDList[i]>0.5)):LowdphiControlRegion.addSingleSystematic("contamUnc"+str(i), 'lnN','contam',1+(ContaminUncForLowdphiRegion[i]/ContaminForLowdphiRegion[i]),'',i)
		for i in range(len(ListOfQCDSysK1)):
			if(ListOfQCDSysK1[i]!='-'):signalRegion.addSingleSystematic("KQCDJ1HT1",'lnN','qcd',float(ListOfQCDSysK1[i]),'',i);
			if(ListOfQCDSysK2[i]!='-'):signalRegion.addSingleSystematic("KQCDJ1HT2",'lnN','qcd',float(ListOfQCDSysK2[i]),'',i);
			if(ListOfQCDSysK3[i]!='-'):signalRegion.addSingleSystematic("KQCDJ1HT3",'lnN','qcd',float(ListOfQCDSysK3[i]),'',i);
			if(ListOfQCDSysK4[i]!='-'):signalRegion.addSingleSystematic("KQCDJ2HT1",'lnN','qcd',float(ListOfQCDSysK4[i]),'',i);
			if(ListOfQCDSysK5[i]!='-'):signalRegion.addSingleSystematic("KQCDJ2HT2",'lnN','qcd',float(ListOfQCDSysK5[i]),'',i);
			if(ListOfQCDSysK6[i]!='-'):signalRegion.addSingleSystematic("KQCDJ2HT3",'lnN','qcd',float(ListOfQCDSysK6[i]),'',i);
			if(ListOfQCDSysK7[i]!='-'):signalRegion.addSingleSystematic("KQCDJ3HT1",'lnN','qcd',float(ListOfQCDSysK7[i]),'',i);
			if(ListOfQCDSysK8[i]!='-'):signalRegion.addSingleSystematic("KQCDJ3HT2",'lnN','qcd',float(ListOfQCDSysK8[i]),'',i);
			if(ListOfQCDSysK9[i]!='-'):signalRegion.addSingleSystematic("KQCDJ3HT3",'lnN','qcd',float(ListOfQCDSysK9[i]),'',i);
			if(ListOfQCDSysK10[i]!='-'):signalRegion.addSingleSystematic("KQCDJ4HT2",'lnN','qcd',float(ListOfQCDSysK10[i]),'',i);
			if(ListOfQCDSysK11[i]!='-'):signalRegion.addSingleSystematic("KQCDJ4HT3",'lnN','qcd',float(ListOfQCDSysK11[i]),'',i);
			if(ListOfQCDSysK12[i]!='-'):signalRegion.addSingleSystematic("KQCDJ5HT2",'lnN','qcd',float(ListOfQCDSysK12[i]),'',i);
			if(ListOfQCDSysK13[i]!='-'):signalRegion.addSingleSystematic("KQCDJ5HT3",'lnN','qcd',float(ListOfQCDSysK13[i]),'',i);
			if(ListOfQCDSysK14[i]!='-'):signalRegion.addSingleSystematic("KQCDHT1MHT1",'lnN','qcd',float(ListOfQCDSysK14[i]),'',i);
			if(ListOfQCDSysK15[i]!='-'):signalRegion.addSingleSystematic("KQCDHT1MHT2",'lnN','qcd',float(ListOfQCDSysK15[i]),'',i);
			if(ListOfQCDSysK16[i]!='-'):signalRegion.addSingleSystematic("KQCDHT2MHT1",'lnN','qcd',float(ListOfQCDSysK16[i]),'',i);
			if(ListOfQCDSysK17[i]!='-'):signalRegion.addSingleSystematic("KQCDHT2MHT2",'lnN','qcd',float(ListOfQCDSysK17[i]),'',i);
			if(ListOfQCDSysK18[i]!='-'):signalRegion.addSingleSystematic("KQCDHT2MHT3",'lnN','qcd',float(ListOfQCDSysK18[i]),'',i);
			if(ListOfQCDSysK19[i]!='-'):signalRegion.addSingleSystematic("KQCDHT2MHT4",'lnN','qcd',float(ListOfQCDSysK19[i]),'',i);
			if(ListOfQCDSysK20[i]!='-'):signalRegion.addSingleSystematic("KQCDHT3MHT1",'lnN','qcd',float(ListOfQCDSysK20[i]),'',i);
			if(ListOfQCDSysK21[i]!='-'):signalRegion.addSingleSystematic("KQCDHT3MHT2",'lnN','qcd',float(ListOfQCDSysK21[i]),'',i);
			if(ListOfQCDSysK22[i]!='-'):signalRegion.addSingleSystematic("KQCDHT3MHT3",'lnN','qcd',float(ListOfQCDSysK22[i]),'',i);
			if(ListOfQCDSysK23[i]!='-'):signalRegion.addSingleSystematic("KQCDHT3MHT4",'lnN','qcd',float(ListOfQCDSysK23[i]),'',i);
			if(ListOfMCCSys[i]!='-'):signalRegion.addSingleSystematic("KQCDMCCorr",'lnN','qcd',float(ListOfMCCSys[i]),'',i);
	######################################################################
	######################################################################
	# 4. Write Cards
	######################################################################
	######################################################################	

	signalRegion.writeCards( odir );
	#if options.allBkgs or options.llpOnly or  (options.tauOnly and  options.llpOnly) or options.tauOnly: SLcontrolRegion.writeCards( odir );
	# if options.allBkgs or options.tauOnly: HadcontrolRegion.writeCards( odir );
	#if options.allBkgs or options.zvvOnly: sphotonRegion.writeCards( odir );
	#if options.allBkgs or options.qcdOnly: 
	LowdphiControlRegion.writeCards( odir );
		#LowdPhiLowMHTControlRegion.writeCards(odir);
		#HighdPhiLowMHTControlRegion.writeCards(odir)
