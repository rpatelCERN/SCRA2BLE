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
#AR-180426: When parse_args() returns from parsing this command line,options.signal will be "SMSqqqq1000", options.fastsim will be "false" in default case
#AR-180426:sample command to run this script, coming from analysisBuilderCondor.py will be: python analysisBuilderCondor.py --signal T1tttt --mGo 1500 --mLSP 100 --fastsim --realData  --tag allBkgs
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option("--signal", dest="signal", default = 'SMSqqqq1000',help="mass of LSP", metavar="signal")
parser.add_option("--tag", dest="tag", default = 'SinglePhoton1',help="mass of LSP", metavar="tag")
parser.add_option("--mu", dest="mu", default = 1.,help="mass of LSP", metavar="mu")
parser.add_option("--lumi", dest="lumi", default = 10.,help="mass of LSP", metavar="lumi")
parser.add_option('--fastsim', action='store_true', dest='fastsim', default=False, help='no X11 windows')
parser.add_option('--realData',action='store_true', dest='realData', default=False, help='no X11 windows')
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
#options.signal[2:] returns 3rd to end of list(as list index starts from zero)

if __name__ == '__main__':
#AR-180515:This is not the sms we use, as we have options.fastsim=true.
	sms = "SMS"+options.signal[2:]+options.mGo;
	print "options.signal[2:] ", options.signal[2:]
#AR-180426:when "fastsim" is true, sms=T1tttt_1500_100
	if options.fastsim: sms = options.signal+'_'+options.mGo+'_'+options.mLSP;
	tag = options.tag;
	lumi = float(options.lumi);
	signalmu = float(options.mu);
#AR-180426: odir=testCards-allBkgs-T1tttt_1500_100-35.9-mu0.0----Name of output directory
	odir = '/nfs/data39/cms/rish/RA2Moriond/testCards-%s-%s-%1.1f-mu%0.1f/' % ( tag,sms, lumi, signalmu );
#AR-180426: idir=inputHistograms/histograms_35.9fb/. Here are various background estimates.
	idir = 'inputHistograms/histograms_%1.1ffb/' % ( ((lumi)) );
	#idir = 'inputHistograms/MCForBinOptimization/';
#AR-180426:os.path.exists(odir):Return True if path refers to an existing path. Returns False for broken symbolic links.
#forcefully remove directory if it exists 
	if os.path.exists(odir): os.system( "rm -rf %s" % (odir) );
#Symbol: os.makedirs(path[, mode]), ex. os.makedirs( path, 0755 ). Default mode is octal
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
		signaldirtag += "/fastsimSignalScan";
		if "T2bb" in sms:  signaldirtag ="inputHistograms/fastsimSignalT2bb"
		if "T1tttt" in sms:  signaldirtag ="inputHistograms/fastsimSignalT1tttt"
		if "T1bbbb" in sms:  signaldirtag ="inputHistograms/fastsimSignalT1bbbb"
		if "T1qqqq" in sms:  signaldirtag ="inputHistograms/fastsimSignalT1qqqq"
		if "T5qqqqVV" in sms:  signaldirtag ="inputHistograms/fastsimSignalT5qqqqVV"
		#if ("T1" in sms or "T5qqqqVV" in sms): signaldirtag +="Gluino"
		if ("T2qq" in sms): signaldirtag ="inputHistograms/fastsimSignalT2qq"
		if ("T2tt" in sms): signaldirtag ="inputHistograms/fastsimSignalT2tt"
		if "T1ttbb" in sms : signaldirtag="/fastsimSignalScanT1ttbb/"
		if "T1tbtb" in sms : signaldirtag="/fastsimSignalScanT1tbtb/"			
		if "T1tbtb" in sms : signaldirtag="/fastsimSignalScanT1tbtb/"			
		if "T1tbtbT1tbbbT1bbbb" in sms : signaldirtag="/fastsimSignalScanT1tbtbT1tbbbT1bbbb/"			
		if "T1tbtbT1tbttT1tttt" in sms : signaldirtag="/fastsimSignalScanT1tbtbT1tbttT1tttt/"			

#AR-180515: For Moriond run, following was the signaldirtag  
		#signaldirtag="inputHistograms/Run2ProductionV12/"

		#signaldirtag="/fdata/hepx/store/user/rish/CombineCards/Run2ProductionV11new/"
		#signaldirtag="/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/"#signaldirtag="/fdata/hepx/store/user/rish/CombineCards/Run2ProductionV11new/"
		#signaldirtag="./inputHistograms/fastsimSignalT1bbbb/"
	else: signaldirtag ="inputHistograms/FullSim"
	#signaldirtag ="inputHistograms/MCForBinOptimization/"
	#signaldirtag ="inputHistograms/MCNominalBinning/"
	#AR-180427:when "fastsim" is true, sms=T1tttt_1500_100. Hence, signaltag=RA2bin_proc_T1tttt_1500_100
	#print "Data_List ", Data_List
	signaltag = "RA2bin_proc_"+sms+"_MC2017";
	#signaltag = "RA2bin_signal_"+sms;
	parse=sms.split('_')
	model=parse[0]
	#print parse
#AR-180427:Here signaltag becomes "RA2bin_proc_T1tttt_1500_100_fast
	#if options.fastsim: 
	signaltag+="_fast"
	print signaldirtag+"/%s.root" %signaltag
#AR-180427:Name of input histogram file for FastSim:"RA2bin_proc_T1tttt_1500_100_fast.root" from directory "root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/"
	signal_inputfile =TFile.Open(signaldirtag+"/%s.root" %signaltag);
#AR-180427:Now file "RA2bin_proc_T1tttt_1500_100_fast.root" has histograms for nominal expected signal yield in search bins and that after applying various uncertainties. Name of these histograms are of type RA2bin_T1tttt_1500_100_fast_*. Hence signaltag is defined as below.
#AR-180515:signaltag=RA2bin_T1tttt_1500_100_fast
	#signaltag="RA2bin_"+sms+"_fast";
	signaltag="RA2bin_"+sms+"_MC2017_fast";
	print "%s_nominal" %signaltag
#AR-180427:Gets signal nominal yield histogram "RA2bin_T1tttt_1500_100_fast_nominal" and scale it to "lumi*1000". This implies histogram root file corresponds to lumi of 1/pb.
	CorrSigHist=signal_inputfile.Get("%s_nominal" %signaltag)
	CorrSigHist.Scale(lumi*1000.)	
	#genMHTCorr(signaldirtag,signaltag,lumi)		
	#if "T2tt" in sms or "T1tttt" in sms or "T5qqqqVV" in sms or "T1t" in sms: 
		#CorrSigHist=LeptonCorr(signaldirtag,options.signal,lumi, int(options.mGo), int(options.mLSP))   #AR-180427:returns signal contamination, need to look in carefully.
	#MHTSyst=genMHTSyst(signaldirtag,signaltag,lumi)	
#AR-180515: Return bin labels of histogram like ['NJets0_BTags0_MHT0_HT0', 'NJets0_BTags0_MHT0_HT1'....]
	tagsForSignalRegion = binLabelsToList(CorrSigHist);	
	#print "tagsForSignalRegion ",tagsForSignalRegion
#AR-180427: reads data prediction histograms related to LL:totalPred_LL, avgWeight_0L1L,ControlStatUnc. 
	contributionsPerBin = [];
	Data_List=[]
	for i in range(len(tagsForSignalRegion)): 	
		tmpcontributions = [];
		tmpcontributions.append('sig');
		tmpcontributions.append('WTop');
		tmpcontributions.append('zvv')
		tmpcontributions.append('qcd')
		contributionsPerBin.append(tmpcontributions) #AR: contributionsPerBin has saved seven elements' list per bin
	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)
	if options.realData:
        	DataHist_In=TFile("inputHistograms/histograms_%1.1ffb/RA2bin_signalUnblind.root" %lumi)
        	Data_Hist=DataHist_In.Get("RA2bin_data")
        	Data_List=binsToList(Data_Hist) # creates a list of bin contents

	LLPlusHadTauAvg_file=TFile(idir+"/InputsForLimits_data_formatted_LLPlusHadTau.root");
	#LLPlusHadTau_file = TFile(idir+"/LLPlusHadTauPrediction.root");
	LLPlusHadTauPrediction_Hist=LLPlusHadTauAvg_file.Get("totalPred_LLPlusHadTau")
	LLPlusHadTauControlStatistics=LLPlusHadTauAvg_file.Get("DataCSStatistics")		
	LLPlusHadTauControlStatUnc_Hist=LLPlusHadTauAvg_file.Get("DataCSStatErr")
	LLPlusHadTauTF=LLPlusHadTauAvg_file.Get("LLPlusHadTauTF")
	LLPlusHadTauTFStatUnc=LLPlusHadTauAvg_file.Get("LLPlusHadTauTFErr")
	LLPlusHadTauSysBMistagDn=LLPlusHadTauAvg_file.Get("totalPredBMistagDown_LLPlusHadTau")
	LLPlusHadTauSysJECDn=LLPlusHadTauAvg_file.Get("totalPredJECSysDown_LLPlusHadTau")
	LLPlusHadTauSysMTDn=LLPlusHadTauAvg_file.Get("totalPredMTSysDown_LL")	
	LLPlusHadTauAccPDFSysDn=LLPlusHadTauAvg_file.Get("totalPredPDFDown_LLPlusHadTau")
	LLPlusHadTauQScaleSysDn=LLPlusHadTauAvg_file.Get("totalPredScaleDown_LLPlusHadTau")
	LLPlusHadTauEleIDSysDn=LLPlusHadTauAvg_file.Get("totalPredEleIDSysDown_LL")	
	LLPlusHadTauEleSysIsoDn=LLPlusHadTauAvg_file.Get("totalPredEleIsoSysDown_LL")	
	LLPlusHadTauEleSysReco=LLPlusHadTauAvg_file.Get("totalPredEleRecoSysDown_LL")	
	#/print LLPlusHadTauEleSysRecoDn.GetBinContent(1)
	LLPlusHadTauSysIsoDn=LLPlusHadTauAvg_file.Get("totalPredMuIsoSysDown_LL")	
	LLPlusHadTauSysMuIdDn=LLPlusHadTauAvg_file.Get("totalPredMuIDSysDown_LL")	
	LLPlusHadTauSysMuRecoDn=LLPlusHadTauAvg_file.Get("totalPredMuRecoSysDown_LL")	
# reads nominal data prediction
	#HERE ADD Bin Errors for the Had Tau Stat Error
	DYinputfile = TFile(idir+"/ZinvHistos.root")
	ZPred=DYinputfile.Get("ZinvBGpred")
	ZRatios=DYinputfile.Get("hzvvTF")
	GammaObs=DYinputfile.Get("hzvvgJNobs")
	#ZgammaErrUp=DYinputfile.Get("hzvvgJZgRerrUp");
	#ZgammaErrDn=DYinputfile.Get("hzvvgJZgRerrLow");
#AR-180427: various Z to nu nu prediction histograms
	ZNBCorrelUp=DYinputfile.Get("hzvvNbCorrelUp")
	ZNBCorrelDn=DYinputfile.Get("hzvvNbCorrelLow")
	GammaETErr=DYinputfile.Get("hzvvgJEtrgErr")
	FdirErrUp=DYinputfile.Get("hgJFdirErrUp")
	FdirErrDn=DYinputfile.Get("hgJFdirErrLow")
	GammaPurityErr=DYinputfile.Get("hzvvgJPurErr");
	#DoubleRatioErrUp=DYinputfile.Get("hzvvZgDRerrUp");
	#DoubleRatioErrDn=DYinputfile.Get("hzvvZgDRerrLow");
	ZScaleErr=DYinputfile.Get("hzvvScaleErr");
	DYStatErr=DYinputfile.Get("hzvvDYstat");
	DYPurErr=DYinputfile.Get("hzvvDYsysPur");
	DYKinErr=DYinputfile.Get("hzvvDYsysKin");
	DYNJExtrapErrUp=DYinputfile.Get("hzvvDYMCerrUp");
	DYNJExtrapErrDn=DYinputfile.Get("hzvvDYMCerrLow");
	#for i in range(1,DYNJExtrapErrDn.GetNbinsX()+1):	
		#ZgammaErrDn.SetBinContent(i,1.0/ZgammaErrDn.GetBinContent(i))
		#DYNJExtrapErrDn.SetBinContent(i,1.0/DYNJExtrapErrDn.GetBinContent(i))
		#DoubleRatioErrDn.SetBinContent(i,1.0/DoubleRatioErrDn.GetBinContent(i))
#AR-180515:HadTauStatUnc saves (1+stat_error/bincontent) error if prediction is non zero, else saves 1+stat_error
	# QCD R+$
#AR-180427: various QCD prediction histograms
	ratesForSignalRegion_QCDList = [];
	QCDInputFile=TFile(idir+"/QcdPredictionRandS.root")
	qcdCV=QCDInputFile.Get("PredictionCV")
	qcdNJetUnc=QCDInputFile.Get("PredictionNJet")
	if not options.realData:
		for i in range(signalRegion._nBins): #174, (0-173)
			srobs=(ZPred.GetBinContent(i+1)+LLPlusHadTauPrediction_Hist.GetBinContent(i+1)+(qcdCV.GetBinContent(i+1)))
			Data_List.append(srobs)
	#for i in range(len(tagsForSignalRegion)):
		#ratesForSignalRegion_QCDList.append(qcdCV.GetBinContent(i+1))
	#AR-180427: ''' provides multiple line indentation. Indent leading ''' properly to avoid indentation error.
#AR-180427: Creates empty list contributionsPerBin here
#AR-180427: odir=testCards-allBkgs-T1tttt_1500_100-35.9-mu0.0
# Creates file testCards-allBkgs-T1tttt_1500_100-35.9-mu0.0/yields.root with histograms for data, 4 backgrounds and signal
	f = TFile(odir+'yields.root', 'recreate')
	data = TH1F( 'data', 'data', 174, 0, 174 )
	qcd = TH1F( 'QCD', 'QCD', 174, 0, 174 )
	zvv = TH1F( 'Zvv', 'Zvv', 174, 0, 174 )
	ll = TH1F( 'LL', 'LL', 174, 0, 174 )
	tau = TH1F( 'tau', 'tau', 174, 0, 174 )
	sig = TH1F( 'sig', 'sig', 174, 0, 174 )
#AR-180515: tagsForSignalRegion have bin labels of histogram like ['NJets0_BTags0_MHT0_HT0', 'NJets0_BTags0_MHT0_HT1'....]
	#print " contributionsPerBin ",contributionsPerBin
	#*AR:180515- creates instance of searchRegion class(signalRegion ), which will be a list of singleBins, with each single bin being referred by name='signali', tag='NJets0_BTags0_MHT0_HT1' etc., binLabels=tmpcontributions, index=bin number, rate=[], allLines = []
	#print "signalRegion_nbins ",signalRegion._nBins #174
	#print "signalRegion_binLabels ",signalRegion._binLabels #list of contributions
	#print "signalRegion_singleBinTags ",signalRegion._singleBinTags #binlabels from tagsForSignalRegion

	signalRegion_Rates = [];
	signalRegion_Obs = [];
#*AR:180515-Reads data histogram containing number of events per search bin
	for i in range(signalRegion._nBins): #174, (0-173)
		tmpList = [];
		srobs = 0;
#tmpList has signal yield, LL prediction, it's avg TF, hadtau prediction, 0.25, Z prediction and QCD prediction

		tmpList.append(CorrSigHist.GetBinContent(i+1)) #signal nominal yield
		#if LLPlusHadTauPrediction_Hist.GetBinContent(i+1)>0.0:
		tmpList.append(LLPlusHadTauPrediction_Hist.GetBinContent(i+1))
		#else:
		#tmpList.append(LLPlusHadTauTF.GetBinContent(i+1))
		#tmpList.append(LLAvgHeight_Hist.GetBinContent(i+1))
#		tmpList.append(HadTauPrediction.GetBinContent(i+1))
		#tmpList.append(0.25) 
		#if GammaObs.GetBinContent(i+1)>0.0:
		tmpList.append(ZPred.GetBinContent(i+1)) 
		#else: tmpList.append(ZRatios.GetBinContent(i+1))
		tmpList.append( qcdCV.GetBinContent(i+1) );
		#srobs=(ZPred.GetBinContent(i+1)+LLPrediction_Hist.GetBinContent(i+1)+HadTauPrediction.GetBinContent(i+1)+(qcdCV.GetBinContent(i+1)))
		#AR-180515: Just filling bin contents from bkg predictions. I think the purpose is to adjust bin centre.
		qcd.Fill(i+.5,  qcdCV.GetBinContent(i+1))
		zvv.Fill(i+.5, ZPred.GetBinContent(i+1))
		#ll.Fill(i+.5, + LLPrediction_Hist.GetBinContent(i+1))
		#tau.Fill(i+.5, HadTauPrediction.GetBinContent(i+1))
#AR-180515:sig histogram is now the one scaled to 35.9/fb and not corresponding to 1/pb 	
		sig.Fill(i+.5,CorrSigHist.GetBinContent(i+1)*signalmu)
		#randPois=TRandom3(random.randint(1,10000000))
		#srobs=randPois.Poisson(srobs)
		srobs=Data_List[i] # dta events in ith bin
#tmpList has LL prediction, it's avg TF, hadtau prediction, 0.25, Z prediction and QCD prediction
		signalRegion_Rates.append(tmpList)
		signalRegion_Obs.append(srobs) # dta events in ith bin
		data.Fill(i+.5, srobs)

	signalRegion.fillRates(signalRegion_Rates ); # fills signal yield, LL prediction, it's avg TF, hadtau prediction, 0.25, Z prediction and QCD prediction in all 174 bins. 
	signalRegion.setObservedManually(signalRegion_Obs) # dta events in all 174 bins
	#*AR:180515- signalRegion is instance of searchRegion class, which will be a list of singleBins, with each single bin being referred by name='signali', tag='NJets0_BTags0_MHT0_HT1' etc., binLabels=tmpcontributions(length=174*7), index=bin number, rate=signalRegion_Rates.

	signalRegion.writeRates();
        f.Write()
	f.Close() #closes yields.root with data, signal and background histograms
	########################

	#Signal Systematics
	
	#######################
	#Get Histograms:
#AR-180516:Gets various systematics histograms associated to signal nominal yield histogram "RA2bin_T1tttt_1500_100_fast_nominal"
#AR-180515:signaltag=RA2bin_T1tttt_1500_100_fast
						
	signalSysPrefireUp=signal_inputfile.Get(signaltag+"_prefireuncUp");
	signalSysPrefireDown=signal_inputfile.Get(signaltag+"_prefireuncDown");
	signalSysISRUp=signal_inputfile.Get(signaltag+"_isotrackuncUp");
	signalSysISRDown=signal_inputfile.Get(signaltag+"_isotrackuncDown");
	signalSysSFUp=signal_inputfile.Get(signaltag+"_btagSFuncUp")	
	signalSysSFDown=signal_inputfile.Get(signaltag+"_btagSFuncDown")		
	signalSysMisSFUp=signal_inputfile.Get(signaltag+"_mistagSFuncUp")
	signalSysMisSFDown=signal_inputfile.Get(signaltag+"_mistagSFuncDown")
	signalSysTrigSystUp=signal_inputfile.Get(signaltag+"_triguncUp")
	signalSysTrigSystDown=signal_inputfile.Get(signaltag+"_triguncDown")
	signalSysJERUp=signal_inputfile.Get(signaltag+"_JERup")
	signalSysJERDown=signal_inputfile.Get(signaltag+"_JERdown")
	signalSysJECUp=signal_inputfile.Get(signaltag+"_JECup")
	signalSysJECDown=signal_inputfile.Get(signaltag+"_JECdown")
	signalPUUp=signal_inputfile.Get(signaltag+"_puaccuncUp")
	signalPUDown=signal_inputfile.Get(signaltag+"_puaccuncDown")
	signalSysScaleUp=signal_inputfile.Get(signaltag+"_scaleuncUp")
	signalSysScaleDown=signal_inputfile.Get(signaltag+"_scaleuncDown")
	signalMCStatError=signal_inputfile.Get(signaltag+"_MCStatErr")
	signalSysbtagCFuncUp=signal_inputfile.Get(signaltag+"_btagCFuncUp")
	signalSysbtagCFuncDown=signal_inputfile.Get(signaltag+"_btagCFuncDown")
	signalSysctagCFuncUp=signal_inputfile.Get(signaltag+"_ctagCFuncUp")
	signalSysctagCFuncDown=signal_inputfile.Get(signaltag+"_ctagCFuncDown")
	signalSysmistagCFuncUp=signal_inputfile.Get(signaltag+"_mistagCFuncUp")
	signalSysmistagCFuncDown=signal_inputfile.Get(signaltag+"_mistagCFuncDown")
	MHTSyst=signal_inputfile.Get(signaltag+"_MHTSyst")
	LumiUnc=signal_inputfile.Get(signaltag+"_lumiuncUp")
	#JetIdUnc=signal_inputfile.Get(signaltag+"_jetiduncUp")
	TkIsoUncUp=signal_inputfile.Get(signaltag+"_isotrackuncUp")
	TkIsoUncDn=signal_inputfile.Get(signaltag+"_isotrackuncDown")
#AR-180516: addSystematicsLine(self,systype,channel,hist):
#systype=lnN, channel='sig'=signal yield histogram, hist=LumiUnc
	#print "['sig'] ", ['sig']
	signalRegion.addSystematicsLine('lnN',['sig'],LumiUnc)
	#signalRegion.addSystematicsLine('lnN',['sig'],JetIdUnc)	
        #signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.027);
        signalRegion.addSingleSystematic('EvtFilters','lnN',['sig'],1.05);
        signalRegion.addSingleSystematic('JetIDUnc','lnN',['sig'],1.01);
	signalRegion.addSystematicsLine('lnN',['sig'],signalMCStatError);	
	signalRegion.addSystematicsLine('lnU',['sig'],MHTSyst);
	
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalPUUp,signalPUDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysMisSFUp,signalSysMisSFDown)	
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysTrigSystUp,signalSysTrigSystDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],TkIsoUncUp,TkIsoUncDn)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysJERUp,signalSysJERDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysJECUp,signalSysJECDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysScaleUp,signalSysScaleDown)
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysPrefireUp,signalSysPrefireDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysISRUp,signalSysISRDown)	
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysSFUp,signalSysSFDown)	
	##############
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysbtagCFuncUp,signalSysbtagCFuncDown)		
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysctagCFuncUp,signalSysctagCFuncDown)		
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysmistagCFuncUp,signalSysmistagCFuncDown)		

	#Correlate HAD TAU AND LOST LEPTON SYSTEMATICS


	############
#AR-180516:CSZero and HadTauHighW as copy of LLAvgHeight_Hist
#GammaObs=DYinputfile.Get("hzvvgJNobs"), DYinputfile=ZinvHistos.root
	for i in range(len(GammaObs)):GammaObs[i]=GammaObs[i]
	signalRegion.addGammaSystematic(['zvv'],GammaObs,ZRatios )
	#signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],ZgammaErrUp,ZgammaErrDn)
	#signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],DoubleRatioErrUp,DoubleRatioErrDn)
	for i in range(len(ZNBCorrelDn)):
		if DYNJExtrapErrDn.GetBinContent(i)<0.0:DYNJExtrapErrDn.SetBinContent(i,0.01);
		if ZNBCorrelDn.GetBinContent(i)<0.0:ZNBCorrelDn.SetBinContent(i,0.01);
	signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],ZNBCorrelUp,ZNBCorrelDn)
	signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],DYNJExtrapErrUp,DYNJExtrapErrDn)
	signalRegion.addSystematicsLine('lnN',['zvv'],ZScaleErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],GammaPurityErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],DYStatErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],DYPurErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],DYKinErr)	
	#signalRegion.addSystematicsLine('lnN',['zvv'],DYMCStatErr)	
	signalRegion.addSystematicsLine('lnN',['zvv'],GammaETErr)
	#signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],FdirErrUp, FdirErrDn)


	QCDContamUnc=QCDInputFile.Get("PredictionContam")		
	QCDCloseUnc=QCDInputFile.Get("PredictionClosure")		
	QCDStatUnc=QCDInputFile.Get("PredictionStat")		
	QCDPriorUnc=QCDInputFile.Get("PredictionPrior")		
	QCDCoreUp=QCDInputFile.Get("PredictionCore")	
	#QCDCoreDn=QCDInputFile.Get("PredictionCoreDown")	
	QCDTail=QCDInputFile.Get("PredictionTail")	
	QCDTrigDn=QCDInputFile.Get("PredictionTrigDown")	
	QCDTrigUp=QCDInputFile.Get("PredictionTrigUp")	
	QCDUnCorrel=QCDInputFile.Get("PredictionUncorrelated")
	for i in range(1, 175):
		QCDUnCorrel.GetXaxis().SetBinLabel(i, "QCDUncorrel"+CorrSigHist.GetXaxis().GetBinLabel(i))
		#CorrelLabel=CorrSigHist.GetXaxis().GetBinLabel(i).split("_")
		#print CorrelLabel
		#qcdNJetUnc.GetXaxis().SetBinLabel(i, "QCDNJetFullyCorrelated");	
		#QCDLabel="QCDCoreUnc%s_%s_%s" %(CorrelLabel[1], CorrelLabel[2], CorrelLabel[3])
		#QCDCoreUp.GetXaxis().SetBinLabel(i, QCDLabel);
		#QCDTail.GetXaxis().SetBinLabel(i, "QCDTail");
	#signalRegion.addSystematicsLine('lnN', ['qcd'], qcdNJetUnc);
	signalRegion.addSystematicsLine('lnN',['qcd'], QCDUnCorrel);
	signalRegion.addSystematicsLine('lnN',['qcd'], QCDTail);
        signalRegion.addSystematicsLine('lnN',['qcd'],QCDCoreUp)

	signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauSysMTDn)
	signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauSysIsoDn)
	signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauSysMuIdDn)

	signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauEleSysIsoDn)
	signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauEleIDSysDn)
	signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauEleSysReco)
	signalRegion.addGammaSystematic(['WTop'],LLPlusHadTauControlStatistics,LLPlusHadTauTF)


	signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauTFStatUnc)
	signalRegion.addSystematicsLine('lnN',['WTop'],LLPlusHadTauSysJECDn)
	signalRegion.addSystematicsLine('lnN',['WTop'],LLPlusHadTauSysBMistagDn)
	signalRegion.addSystematicsLine('lnN',['WTop'],LLPlusHadTauAccPDFSysDn)
	signalRegion.addSystematicsLine('lnN',['WTop'],LLPlusHadTauQScaleSysDn)

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
	#LowdphiControlRegion.writeCards( odir );
		#LowdPhiLowMHTControlRegion.writeCards(odir);
		#HighdPhiLowMHTControlRegion.writeCards(odir)
