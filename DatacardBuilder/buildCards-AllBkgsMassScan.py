from ROOT import *
import os
import math
#import sys
from searchRegion import *
from singleBin import *
from cardUtilities import *
import random
from optparse import OptionParser
#from GenMHTCorrection import *
from SignalMergePeriods import *
import argparse

#########################################################################################################
## to do:
## .......
#########################################################################################################
#options.signal[2:] returns 3rd to end of list(as list index starts from zero)
def NominalSignal(inputfile,signal,mGo,mLSP,yearsToMerge,RunLumi):
	sms="%s_%s_%s" %(signal, mGo,mLSP)
	MergedFullRun2=MergeSignal(inputfile,sms,yearsToMerge,RunLumi);
	MergedFullRun2.SetName("RA2bin_%s_fast_nominalOrig" %(sms))	
	MHTCorr_Unc=[]
	if "T1tttt" in signal or "T2tt" in signal or "T5qqqqVV" in signal:MHTCorr_Unc=SubstractSignalContamination(signaldirtag,signal,mGo, mLSP,yearsToMerge,RunLumi)
	else:MHTCorr_Unc=MHTSystematicGenMHT(signaldirtag,sms, yearsToMerge,RunLumi);
	return MHTCorr_Unc
def WriteSignalSystematics(signaldirtag,signal,mGo,mLSP,yearsToMerge,RunLumi,searchRegion):
	sms="%s_%s_%s" %(signal, mGo,mLSP)
	MergedNominal=MergeSignal(signaldirtag,sms,yearsToMerge,RunLumi);
	#MergedNominal.SetName("NominalOrig")
	#MergedNominal.SetDirectory(0)
        SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(sms))
	#MCStatErr=TH1D();#RA2bin_T1tttt_950_500_MC2016_fast_MCStatErr	
	MCStatErr=SigTempFile.Get("RA2bin_%s_MC2016_fast_MCStatErr" %sms);
	MCStatErr.Reset();
	for i in range(1, MergedNominal.GetNbinsX()+1):
		#MCStatErr.GetXaxis().SetBinLabel(i, "MCStatErr"+MCStatErr.GetXaxis().GetBinLabel(i))
		StatErr=MergedNominal.GetBinError(i);
		if StatErr==0:StatErr=1.0;
		else:
			StatErr=1.0+(StatErr/MergedNominal.GetBinContent(i))
		MCStatErr.SetBinContent(i, StatErr);
	#Symmetric Norm Uncertainties
	signalRegion.addSystematicsLine('lnN',['sig'], MCStatErr);
	SigTempFile.Close();
	LumiUnc=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"lumiuncUp",MergedNominal,True)							
	JetIDUnc=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"jetiduncUp",MergedNominal,True)
	IsoTrackUnc=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isotrackuncUp",MergedNominal,True)
	PrefireUncUp=MergeUncPreFireCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"prefireuncUp",MergedNominal,True)
	PrefireUncDown=MergeUncPreFireCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"prefireuncDown",MergedNominal,False)
	ISRUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isruncUp",MergedNominal,True)
	ISRUncDown=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isruncDown",MergedNominal,False)
	TrigUnc=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"triguncUp",MergedNominal)							
	TrigSysUnc=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"trigsystuncUp;",MergedNominal)							
	searchRegion.addSystematicsLine('lnN',['sig'],LumiUnc)
	searchRegion.addSystematicsLine('lnN',['sig'],JetIDUnc)	
	searchRegion.addSystematicsLine('lnN',['sig'],IsoTrackUnc)	
	searchRegion.addSystematicsLine('lnN',['sig'],TrigUnc)	
	searchRegion.addSystematicsLine('lnN',['sig'],TrigSysUnc)	
	PUUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"puuncUp",MergedNominal,True)	
	#searchRegion.addSystematicsLine('lnN',['sig'],PUUncUp)	
	PUUncDown=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"puuncDown",MergedNominal,False)	
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],PUUncUp,PUUncDown)	
	ScaleUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncUp",MergedNominal)
	JERUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JERup",MergedNominal)
	JECUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JECup",MergedNominal)

	BTagSFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncUp",MergedNominal)
	MisTagSFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncUp",MergedNominal)
	CTagCFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"ctagCFuncUp",MergedNominal)
	BTagCFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagCFuncUp",MergedNominal)
	MisTagCFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagCFuncUp",MergedNominal)

	ScaleUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncDown",MergedNominal)
	JERUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JERdown",MergedNominal)
	JECUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JECdown",MergedNominal)
	BTagSFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncDown",MergedNominal)
	MisTagSFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncDown",MergedNominal)
	BTagCFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagCFuncDown",MergedNominal)
	CTagCFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"ctagCFuncDown",MergedNominal)
	MisTagCFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagCFuncDown",MergedNominal)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],MisTagCFUncDown,MisTagCFUncUp)	
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],BTagCFUncDown,BTagCFUncUp)	
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],CTagCFUncDown,CTagCFUncUp)	
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],MisTagSFUncDown,MisTagSFUncUp)	
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],BTagSFUncDown,BTagSFUncUp)	
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],JERUncDown,JERUncUp)	
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],JECUncDown,JECUncUp)	
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],ScaleUncDown,ScaleUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],ISRUncDown,ISRUncUp)	
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],PrefireUncDown,PrefireUncUp)	
	
def WriteZSystematics(inputfile,CSSystematics,SymSystematics,AsymSystematics,signalRegion):
	Z_file=TFile.Open(inputfile);	
	GammaObs=Z_file.Get(CSSystematics[1])
	#GammaObs.Scale(61.9*1000./(35916.403 +41521.425+21000.905+38196.951))#####BE CAREFUL This is hard coded
	ZRatios=Z_file.Get(CSSystematics[0])
	signalRegion.addGammaSystematic(['zvv'],GammaObs,ZRatios )
	for z in SymSystematics:
		hsyst=Z_file.Get(z)
		signalRegion.addSystematicsLine('lnN',['zvv'],hsyst)
	#print GammaObs.GetBinContent(1),ZRatios.GetBinContent(1)
	for i in range(len(AsymSystematics)):
		if i%2==0:
			UpSyst=Z_file.Get(AsymSystematics[i+1])
			DownSyst=Z_file.Get(AsymSystematics[i])
			print AsymSystematics[i],AsymSystematics[i-1]
			signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],DownSyst,UpSyst)
	Z_file.Close()
def WriteQCDSystematics(inputfile,ListOfSystematics,signalRegion,tagsForSignalRegion):
	QCD_file=TFile.Open(inputfile);
	for syst in ListOfSystematics:
		hTempSyst=QCD_file.Get(syst)
		if "Uncorrelated" in syst:
			for i in range(1,175):hTempSyst.GetXaxis().SetBinLabel(i,"QCDUncorrel"+tagsForSignalRegion[i-1])			
		signalRegion.addSystematicsLine('lnN',['qcd'], hTempSyst);
	
	QCD_file.Close();
def WriteLostLeptonSystematics(inputfile, ListOfSystematics,signalRegion):
	LLPlusHadTauAvg_file=TFile.Open(inputfile);
	for syst in ListOfSystematics:
		print syst
		hTempSyst=LLPlusHadTauAvg_file.Get(syst)
		#All symmetric systematics for log-normal
		if syst is not "DataCSStatistics" and syst is not "LLPlusHadTauTF":
			signalRegion.addSystematicsLine('lnN',['WTop'],hTempSyst)
			
	LLPlusHadTauControlStatistics=LLPlusHadTauAvg_file.Get("DataCSStatistics")
	#LLPlusHadTauControlStatistics.Scale(61.9*1000./(35916.403 +41521.425+21000.905+38196.951))#####BE CAREFUL This is hard coded
	LLPlusHadTauTF=LLPlusHadTauAvg_file.Get("LLPlusHadTauTF")	
	signalRegion.addGammaSystematic(['WTop'],LLPlusHadTauControlStatistics,LLPlusHadTauTF)
			
	LLPlusHadTauAvg_file.Close()

if __name__ == '__main__':
#AR-180515:This is not the sms we use, as we have options.fastsim=true.
	parser = argparse.ArgumentParser()
	#AR-180426: When parse_args() returns from parsing this command line,options.signal will be "SMSqqqq1000", options.fastsim will be "false" in default case
	#AR-180426:sample command to run this script, coming from analysisBuilderCondor.py will be: python analysisBuilderCondor.py --signal T1tttt --mGo 1500 --mLSP 100 --fastsim --realData  --tag allBkgs
	#parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
	#parser.add_option("--tag", dest="tag", default = 'SinglePhoton1',help="mass of LSP", metavar="tag")
	parser.add_argument("--signal", dest="signal", default = 'SMSqqqq1000',help="mass of LSP", metavar="signal")
	parser.add_argument("--lumi", dest="lumi", default = 10.,help="mass of LSP", metavar="lumi")
	parser.add_argument("--mu", dest="mu", default = 1.,help="mass of LSP", metavar="mu")
	parser.add_argument("--mGo", dest="mGo", default='1000', help="Mass of Gluino", metavar="mGo")
	parser.add_argument("--mLSP", dest="mLSP", default='900', help="Mass of LSP", metavar="mLSP")
	parser.add_argument('--fastsim', action='store_true', dest='fastsim', default=False, help='no X11 windows')
	parser.add_argument('--realData',action='store_true', dest='realData', default=False, help='no X11 windows')
	#parser.add_option('--qcdOnly', action='store_true', dest='qcdOnly', default=False, help='no X11 windows')
	#parser.add_option('--zvvOnly', action='store_true', dest='zvvOnly', default=False, help='no X11 windows')
	#parser.add_option('--tauOnly', action='store_true', dest='tauOnly', default=False, help='no X11 windows')
	#parser.add_option('--llpOnly', action='store_true', dest='llpOnly', default=False, help='no X11 windows')
	#parser.add_option('--allBkgs', action='store_true', dest='allBkgs', default=False, help='no X11 windows')
	options = parser.parse_args()
        #print options
        #exit(0)
	sms = "SMS"+options.signal[2:]+options.mGo;
	print "options.signal[2:] ", options.signal[2:]
#AR-180426:when "fastsim" is true, sms=T1tttt_1500_100
	if options.fastsim: sms = options.signal+'_'+options.mGo+'_'+options.mLSP;
	print options.lumi
	#tag = options.tag;
	lumi = float(options.lumi);
	signalmu = float(options.mu);
#AR-180426: odir=testCards-allBkgs-T1tttt_1500_100-35.9-mu0.0----Name of output directory

	#odir = 'testCards-%s-%s-%1.1f-mu%0.1f/' % ( tag,sms, lumi, signalmu );
	odir = 'testCards-Moriond-%s-%1.1f-mu%0.1f/' % ( sms, lumi, signalmu );
#AR-180426: idir=inputHistograms/histograms_35.9fb/. Here are various background estimates.
	idir = 'inputHistograms/histograms_%1.1ffb/' % ( ((lumi)) );
	print idir
	#idir = 'inputHistograms/MCForBinOptimization/';
#AR-180426:os.path.exists(odir):Return True if path refers to an existing path. Returns False for broken symbolic links.
#forcefully remove directory if it exists 
	if os.path.exists(odir): os.system( "rm -rf %s" % (odir) );
#Symbol: os.makedirs(path[, mode]), ex. os.makedirs( path, 0755 ). Default mode is octal
	os.makedirs(odir);


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
		#signaldirtag="/eo/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/"#signaldirtag="/fdata/hepx/store/user/rish/CombineCards/Run2ProductionV11new/"
		#signaldirtag="./inputHistograms/fastsimSignalT1bbbb/"
	else: signaldirtag ="inputHistograms/FullSim"
	signaldirtag ="root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV16_v6/"
	#signaldirtag ="inputHistograms/MCNominalBinning/"
	#AR-180427:when "fastsim" is true, sms=T1tttt_1500_100. Hence, signaltag=RA2bin_proc_T1tttt_1500_100
	#print "Data_List ", Data_List
	signaltag = "RA2bin_proc_"+sms+"_Merged";
	yearsToMerge=["MC2016","MC2017","MC2018", "MC2018HEM"]
	RunLumi=[ 35916.403 , 41521.425,21000.905,38196.951 ]
        mLSP=int(options.mLSP)
        mGo=int(options.mGo)
	TestNominal=NominalSignal(signaldirtag,options.signal,mGo,mLSP,yearsToMerge,RunLumi)
	#signaltag = "RA2bin_proc_"+sms+"_MC2017";
	#signaltag = "RA2bin_"+sms+"";
	#signaltag = "RA2bin_signal_"+sms+"_Merged";
	parse=sms.split('_')
	model=parse[0]
	#print parse
#AR-180427:Here signaltag becomes "RA2bin_proc_T1tttt_1500_100_fast
	#if options.fastsim: 
	#yearsToMerge=["MC2016","MC2017"]
	#RunLumi=[35900., 101499.]
	#MergedFullRun2=MergeSignal(signaldirtag,sms,yearsToMerge,RunLumi);
	signaltag+="_fast"
	#print MergedFullRun2.Integral()#signaldirtag+"/%s.root" %signaltag
#AR-180427:Name of input histogram file for FastSim:"RA2bin_proc_T1tttt_1500_100_fast.root" from directory "root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/"
	#signal_inputfile =TFile.Open(signaldirtag+"/%s.root" %signaltag);
#AR-180427:Now file "RA2bin_proc_T1tttt_1500_100_fast.root" has histograms for nominal expected signal yield in search bins and that after applying various uncertainties. Name of these histograms are of type RA2bin_T1tttt_1500_100_fast_*. Hence signaltag is defined as below.
#AR-180515:signaltag=RA2bin_T1tttt_1500_100_fast
	#signaltag="RA2bin_"+sms+"_MC2017_fast";
	signaltag="RA2bin_"+sms+"_fast";
	print "%s_nominal" %signaltag
#AR-180427:Gets signal nominal yield histogram "RA2bin_T1tttt_1500_100_fast_nominal" and scale it to "lumi*1000". This implies histogram root file corresponds to lumi of 1/pb.
	#CorrSigHist=signal_inputfile.Get("%s_nominal" %signaltag)
	CorrSigHist=TestNominal[0]#signal_inputfile.Get("%s_nominal" %signaltag)
	CorrSigHist.SetDirectory(0)
	#signal_inputfile.Close();
	
	#CorrSigHist.Scale((lumi*1000.)/(RunLumi[0]+RunLumi[1]+RunLumi[2]+RunLumi[3]))#####BE CAREFUL This is hard coded
	#genMHTCorr(signaldirtag,signaltag,lumi)		
	#if "T2tt" in sms or "T1tttt" in sms or "T5qqqqVV" in sms or "T1t" in sms: 
		#CorrSigHist=LeptonCorr(signaldirtag,options.signal,lumi, int(options.mGo), int(options.mLSP))   #AR-180427:returns signal contamination, need to look in carefully.
	#MHTSyst=genMHTSyst(signaldirtag,signaltag,lumi)	
#AR-180515: Return bin labels of histogram like ['NJets0_BTags0_MHT0_HT0', 'NJets0_BTags0_MHT0_HT1'....]
	tagsForSignalRegion = binLabelsToList(CorrSigHist);	
	#tagsForSignalRegion = binLabelsToList(MergedFullRun2);	
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
        	DataHist_In=TFile.Open("inputHistograms/histograms_%1.1ffb/RA2bin_signalUnblindMerged.root" %lumi)
        	Data_Hist=DataHist_In.Get("RA2bin_data_Unblind")
		Data_Hist.SetDirectory(0);
        	#Data_Hist2017=DataHist_In.Get("RA2bin_data2017")
		#Data_Hist2017.SetDirectory(0);
        	#Data_Hist2018=DataHist_In.Get("RA2bin_data2018")
		#Data_Hist2018.SetDirectory(0);
        	#Data_Hist2018HEM=DataHist_In.Get("RA2bin_data2018HEM")
		#Data_Hist2018HEM.SetDirectory(0);
		#Data_Hist.Add(Data_Hist2017);
		#Data_Hist.Add(Data_Hist2018)
		#Data_Hist.Add(Data_Hist2018HEM)
        	Data_List=binsToList(Data_Hist) # creates a list of bin content	
		DataHist_In.Close();
	LLPlusHadTauAvg_file=TFile.Open(idir+"/InputsForLimits_data_formatted_LLPlusHadTau.root");
	#LLPlusHadTau_file = TFile(idir+"/LLPlusHadTauPrediction.root");
	LLPlusHadTauPrediction_Hist=LLPlusHadTauAvg_file.Get("totalPred_LLPlusHadTau")
	LLPlusHadTauPrediction_Hist.SetDirectory(0)
        #LLPlusHadTauPrediction_Hist.Scale(61.9*1000. /(RunLumi[0]+RunLumi[1]+RunLumi[2]+RunLumi[3]))
	LLPlusHadTauAvg_file.Close();
	#LLPlusHadTauControlStatistics=TH1D()#LLPlusHadTauAvg_file.Get("DataCSStatistics")		
	#LLPlusHadTauControlStatUnc_Hist=TH1D()#LLPlusHadTauAvg_file.Get("DataCSStatErr")
	#LLPlusHadTauTF=TH1D()#LLPlusHadTauAvg_file.Get("LLPlusHadTauTF")
	#LLPlusHadTauTFStatUnc=TH1D()#LLPlusHadTauAvg_file.Get("LLPlusHadTauTFErr")
	#LLPlusHadTauSysBMistagDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredBMistagDown_LLPlusHadTau")
	#LLPlusHadTauSysJECDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredJECSysDown_LLPlusHadTau")
	#LLPlusHadTauSysMTDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredMTSysDown_LL")	
	#LLPlusHadTauAccPDFSysDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredPDFDown_LLPlusHadTau")
	#LLPlusHadTauQScaleSysDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredScaleDown_LLPlusHadTau")
	#LLPlusHadTauEleIDSysDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredEleIDSysDown_LL")	
	#LLPlusHadTauEleSysIsoDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredEleIsoSysDown_LL")	
	#LLPlusHadTauEleSysReco=TH1D()#LLPlusHadTauAvg_file.Get("totalPredEleRecoSysDown_LL")	
	#LLPlusHadTauSysIsoDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredMuIsoSysDown_LL")	
	#LLPlusHadTauSysMuIdDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredMuIDSysDown_LL")	
	#LLPlusHadTauSysMuRecoDn=TH1D()#LLPlusHadTauAvg_file.Get("totalPredMuRecoSysDown_LL")	
	#for key in gDirectory.GetListOfKeys():
	#	if("totalPred_LLPlusHadTau" in key.GetName()):LLPlusHadTauPrediction_Hist=key.ReadObj()
	#	if("DataCSStatistics" in key.GetName()):LLPlusHadTauControlStatistics=key.ReadObj()
	#	if("DataCSStatErr" in key.GetName()):LLPlusHadTauControlStatUnc_Hist=key.ReadObj()
	#	if("LLPlusHadTauTF" in key.GetName()):LLPlusHadTauTF=key.ReadObj()
	#	if("LLPlusHadTauTFErr" in key.GetName()):LLPlusHadTauTFStatUnc=key.ReadObj()
	#	if("totalPredBMistagDown_LLPlusHadTau" in key.GetName()):LLPlusHadTauSysBMistagDn=key.ReadObj()
	#	if("totalPredJECSysDown_LLPlusHadTau" in key.GetName()):LLPlusHadTauSysJECDn=key.ReadObj()
	#	if("totalPredMTSysDown_LL" in key.GetName()):LLPlusHadTauSysMTDn=key.ReadObj()
	#	if("totalPredPDFDown_LLPlusHadTau" in key.GetName()):LLPlusHadTauAccPDFSysDn=key.ReadObj()
	#	if("totalPredScaleDown_LLPlusHadTau" in key.GetName()):LLPlusHadTauQScaleSysDn=key.ReadObj()
	#	if("totalPredEleIDSysDown_LL" in key.GetName()):LLPlusHadTauEleIDSysDn=key.ReadObj()
	#	if("totalPredEleIsoSysDown_LL" in key.GetName()):LLPlusHadTauEleSysIsoDn=key.ReadObj()
	#	if("totalPredEleRecoSysDown_LL" in key.GetName()):LLPlusHadTauEleSysReco=key.ReadObj()
	#	if("totalPredMuIsoSysDown_LL" in key.GetName()):LLPlusHadTauSysIsoDn=key.ReadObj()
	#	if("totalPredMuIDSysDown_LL" in key.GetName()):LLPlusHadTauSysMuIdDn=key.ReadObj()
	#	if("totalPredMuRecoSysDown_LL" in key.GetName()):LLPlusHadTauSysMuRecoDn=key.ReadObj()
	#/print LLPlusHadTauEleSysRecoDn.GetBinContent(1)
	
# reads nominal data prediction
	#HERE ADD Bin Errors for the Had Tau Stat Error
		
#AR-180515:HadTauStatUnc saves (1+stat_error/bincontent) error if prediction is non zero, else saves 1+stat_error
	# QCD R+$
#AR-180427: various QCD prediction histograms
	ratesForSignalRegion_QCDList = [];
	QCDInputFile=TFile.Open(idir+"/QcdPredictionRandS.root")
	qcdCV=QCDInputFile.Get("PredictionCV")
	#qcdCV.Scale(61.9*1000. /(RunLumi[0]+RunLumi[1]+RunLumi[2]+RunLumi[3]))
	qcdCV.SetDirectory(0)
	QCDInputFile.Close();
	DYinputfile = TFile.Open(idir+"ZinvHistos.root","READ")
	ZPred=DYinputfile.Get("ZinvBGpred")
	#ZPred.Scale(61.9*1000. /(RunLumi[0]+RunLumi[1]+RunLumi[2]+RunLumi[3]))
	ZPred.SetDirectory(0);
	DYinputfile.Close()
	#ZRatios=TH1D()#DYinputfile.Get("hzvvTF")
	#GammaObs=TH1D()#DYinputfile.Get("hzvvgJNobs")
	#ZNBCorrelUp=TH1D()#DYinputfile.Get("hzvvNbCorrelUp")
	#ZNBCorrelDn=TH1D()#DYinputfile.Get("hzvvNbCorrelLow")
	#GammaETErr=TH1D()#DYinputfile.Get("hzvvgJEtrgErr")
	#FdirErrUp=TH1D()#DYinputfile.Get("hgJFdirErrUp")
	#FdirErrDn=TH1D()#DYinputfile.Get("hgJFdirErrLow")
	#GammaPurityErr=TH1D()#DYinputfile.Get("hzvvgJPurErr")
	#DYNJExtrapErrUp=TH1D()#DYinputfile.Get("hzvvDYMCerrUp")
	#DYNJExtrapErrDn=TH1D()#DYinputfile.Get("hzvvDYMCerrLow")
	#ZScaleErr=TH1D()#DYinputfile.Get("hzvvScaleErr")
	#DYPurErr=TH1D()#DYinputfile.Get("hzvvDYsysPur")
	#DYStatErr=TH1D()#DYinputfile.Get("hzvvDYstat")
	#DYKinErr=TH1D()#DYinputfile.Get("hzvvDYsysKin")
	#ZSystematics=["hzvvTF","hzvvgJNobs","hzvvNbCorrelUp","hzvvNbCorrelLow","hzvvgJEtrgErr","hgJFdirErrUp","hgJFdirErrLow","hzvvgJPurErr","hzvvDYMCerrUp","hzvvDYMCerrLow","hzvvScaleErr","hzvvDYsysPur","hzvvDYstat","hzvvDYsysKin"]
	'''
	for key in gDirectory.GetListOfKeys():
		#print key.ReadObj().GetName()
		if "ZinvBGpred" in key.GetName():ZPred=key.ReadObj()
		if("zvv" in  key.GetName()):
			if "hzvvTF" in key.GetName():ZRatios=key.ReadObj()
			if "hzvvgJNobs" in key.GetName():GammaObs=key.ReadObj()
			if "hzvvNbCorrelUp" in key.GetName():ZNBCorrelUp=key.ReadObj()
			if "hzvvNbCorrelLow" in key.GetName():ZNBCorrelDn=key.ReadObj()
			if "hzvvgJEtrgErr" in key.GetName():GammaETErr=key.ReadObj()
			if "hgJFdirErrUp" in key.GetName():FdirErrUp=key.ReadObj()
			if "hgJFdirErrLow" in key.GetName():FdirErrDn=key.ReadObj()
			if "hzvvgJPurErr" in key.GetName():GammaPurityErr=key.ReadObj()
			if "hzvvDYMCerrUp" in key.GetName():DYNJExtrapErrUp=key.ReadObj()
			if "hzvvDYMCerrLow" in key.GetName():DYNJExtrapErrDn=key.ReadObj()
			if "hzvvScaleErr" in key.GetName():ZScaleErr=key.ReadObj()
			if "hzvvDYsysPur" in key.GetName():DYPurErr=key.ReadObj()
			if "hzvvDYstat" in key.GetName():DYStatErr=key.ReadObj()
			if "hzvvDYsysKin" in key.GetName():DYKinErr=key.ReadObj()
	'''
	#qcdNJetUnc=QCDInputFile.Get("PredictionNJet")
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
	tmpList = [];
	for i in range(signalRegion._nBins): #174, (0-173)
		srobs = 0;
		#tmpList has signal yield, LL prediction, it's avg TF, hadtau prediction, 0.25, Z prediction and QCD prediction
		tmpList = [];

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
	#NominalMHT=signal_inputfile.Get(signaltag+"_nominalOrig")
	#NominalMHT.Scale(lumi*1000.)
	#genMHT=signal_inputfile.Get(signaltag+"_genMHT")
	#genMHT.Scale(lumi*1000.)

	#LLSystematicsList=["LLPlusHadTauTF","DataCSStatistics","LLPlusHadTauTFErr","totalPredBMistagDown_LLPlusHadTau","totalPred_JECSysDown_LLPlusHadTau","totalPredMTWSysDown_LLPlusHadTau","totalPredLepAccSysDown_LLPlusHadTau","totalPredLepAccSysDown_LLPlusHadTau","totalPredEleIDSysDown_LLPlusHadTau","totalPredEleIsoSysDown_LLPlusHadTau","totalPredEleRecoSysDown_LLPlusHadTau","totalPredMuIsoSysDown_LLPlusHadTau","totalPredMuIDSysDown_LLPlusHadTau","totalPredMuRecoSysDown_LLPlusHadTau"]

	#LLSystematicsList=["LLPlusHadTauTF","DataCSStatistics","LLPlusHadTauTFErr","totalPredBMistagDown_LLPlusHadTau","totalPredJECSysDown_LLPlusHadTau","totalPredMTWSysDown_LL","totalPredLepAccSysDown_LLPlusHadTau","totalPredLepAccSysDown_LLPlusHadTau","totalPredEleIDSysDown_LLPlusHadTau","totalPredEleIsoSysDown_LLPlusHadTau","totalPredEleRecoSysDown_LLPlusHadTau","totalPredMuIsoSysDown_LLPlusHadTau","totalPredMuIDSysDown_LLPlusHadTau","totalPredMuRecoSysDown_LLPlusHadTau"]
	#LLSystematicsList=["LLPlusHadTauTF","DataCSStatistics","LLPlusHadTauTFErr","totalPredBMistagDown_LLPlusHadTau","totalPred_JECSysDown_LLPlusHadTau","totalPredMTWSysDown_LLPlusHadTau","totalPredLepAccSysDown_LLPlusHadTau","totalPredLepAccSysDown_LLPlusHadTau","totalPredEleIDSysDown_LLPlusHadTau","totalPredEleIsoSysDown_LLPlusHadTau","totalPredEleRecoSysDown_LLPlusHadTau","totalPredMuIsoSysDown_LLPlusHadTau","totalPredMuIDSysDown_LLPlusHadTau"]
	LLSystematicsList=["LLPlusHadTauTF","DataCSStatistics","LLPlusHadTauTFErr","totalPredBMistagDown_LLPlusHadTau","totalPredJECSysDown_LLPlusHadTau","totalPredMTSysDown_LL","totalPredPDFDown_LLPlusHadTau","totalPredScaleDown_LLPlusHadTau","totalPredEleIDSysDown_LL","totalPredEleIsoSysDown_LL","totalPredEleRecoSysDown_LL","totalPredMuIsoSysDown_LL","totalPredMuIDSysDown_LL","totalPredMuRecoSysDown_LL"]
	
	WriteLostLeptonSystematics(idir+"/InputsForLimits_data_formatted_LLPlusHadTau.root",LLSystematicsList,signalRegion)
	#QCDSystematics=["PredictionCore","PredictionTail","PredictionUncorrelated"]
	QCDSystematics=["PredictionCore","hSyst_tail","PredictionUncorrelated"]
	WriteQCDSystematics(idir+"/QcdPredictionRandS.root",QCDSystematics,signalRegion,tagsForSignalRegion)
	ZSystematicsCS=["hzvvTF","hzvvgJNobs"]
	ZSystematicsSym=["hzvvgJEtrgErr","hzvvgJPurErr","hzvvScaleErr","hzvvDYsysPur","hzvvDYstat","hzvvDYsysKin"]
	ZSystematicsASym=["hzvvNbCorrelUp","hzvvNbCorrelLow","hzvvDYMCerrLow","hzvvDYMCerrUp"]
	WriteZSystematics(idir+"ZinvHistos.root",ZSystematicsCS,ZSystematicsSym,ZSystematicsASym,signalRegion)
	#for i in range(len(GammaObs)):GammaObs[i]=GammaObs[i]
	#signalRegion.addGammaSystematic(['zvv'],GammaObs,ZRatios )
	#signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],ZgammaErrUp,ZgammaErrDn)
	#signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],DoubleRatioErrUp,DoubleRatioErrDn)
	#for i in range(len(ZNBCorrelDn)):
	#	if DYNJExtrapErrDn.GetBinContent(i)<0.0:DYNJExtrapErrDn.SetBinContent(i,0.01);
	#	if ZNBCorrelDn.GetBinContent(i)<0.0:ZNBCorrelDn.SetBinContent(i,0.01);
	#signalRegion.addSystematicsLine('lnN',['zvv'],ZScaleErr)	
	#signalRegion.addSystematicsLine('lnN',['zvv'],GammaPurityErr)	
	#signalRegion.addSystematicsLine('lnN',['zvv'],DYStatErr)	
	#signalRegion.addSystematicsLine('lnN',['zvv'],DYPurErr)	
	#signalRegion.addSystematicsLine('lnN',['zvv'],DYKinErr)	
	#signalRegion.addSystematicsLine('lnN',['zvv'],DYMCStatErr)	
	#signalRegion.addSystematicsLine('lnN',['zvv'],GammaETErr)
	#signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],FdirErrUp, FdirErrDn)

	#signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],ZNBCorrelUp,ZNBCorrelDn)
	#signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],DYNJExtrapErrUp,DYNJExtrapErrDn)
	print qcdCV.GetBinContent(1)
       	signaltag = "RA2bin_proc_"+sms+"_Merged";
	signaltag+="_fast"
	#signal_inputfile =TFile.Open(signaldirtag+"/%s.root" %signaltag);
	signaltag="RA2bin_"+sms+"_fast";
	'''
	LumiUnc=signal_inputfile.Get(signaltag+"_lumiunc")
	TkIsoUncUp=signal_inputfile.Get(signaltag+"_isotrackunc")
	signalSysPrefireUp=signal_inputfile.Get(signaltag+"_prefireunc");
	JetIdUnc=signal_inputfile.Get(signaltag+"_jetidunc")
	signalSysTrigSystUp=signal_inputfile.Get(signaltag+"_trigunc")
	TkIsoUncDn=signal_inputfile.Get(signaltag+"_isotrackuncDown")
	signalSysISRUp=signal_inputfile.Get(signaltag+"_isruncUp");
	signalSysISRDown=signal_inputfile.Get(signaltag+"_isruncDown");
	signalSysPrefireDown=signal_inputfile.Get(signaltag+"_prefireuncDown");
	signalSysTrigSystDown=signal_inputfile.Get(signaltag+"_triguncDown")

	signalSysSFUp=signal_inputfile.Get(signaltag+"_btagSFuncUp")	
	signalSysSFDown=signal_inputfile.Get(signaltag+"_btagSFuncDown")		
	signalSysMisSFUp=signal_inputfile.Get(signaltag+"_mistagSFuncUp")
	signalSysMisSFDown=signal_inputfile.Get(signaltag+"_mistagSFuncDown")
	signalSysJERUp=signal_inputfile.Get(signaltag+"_JERup")
	signalSysJERDown=signal_inputfile.Get(signaltag+"_JERdown")
	signalSysJECUp=signal_inputfile.Get(signaltag+"_JECup")
	signalSysJECDown=signal_inputfile.Get(signaltag+"_JECdown")
	signalPUUp=signal_inputfile.Get(signaltag+"_puaccuncUp")
	signalPUDown=signal_inputfile.Get(signaltag+"_puaccuncDown")
	signalSysScaleUp=signal_inputfile.Get(signaltag+"_scaleuncUp")
	signalSysScaleDown=signal_inputfile.Get(signaltag+"_scaleuncDown")
	#signalMCStatError=signal_inputfile.Get(signaltag+"_MCStatErr")
	signalSysbtagCFuncUp=signal_inputfile.Get(signaltag+"_btagCFuncUp")
	signalSysbtagCFuncDown=signal_inputfile.Get(signaltag+"_btagCFuncDown")
	signalSysctagCFuncUp=signal_inputfile.Get(signaltag+"_ctagCFuncUp")
	signalSysctagCFuncDown=signal_inputfile.Get(signaltag+"_ctagCFuncDown")
	signalSysmistagCFuncUp=signal_inputfile.Get(signaltag+"_mistagCFuncUp")
	signalSysmistagCFuncDown=signal_inputfile.Get(signaltag+"_mistagCFuncDown")
	'''
	MHTSyst=TestNominal[1]#signal_inputfile.Get(signaltag+"_MHTSyst")
	signalRegion.addSystematicsLine('lnU',['sig'],MHTSyst);
	signaltag=options.signal;
	WriteSignalSystematics(signaldirtag,signaltag,mGo,mLSP,yearsToMerge,RunLumi,signalRegion)
	#for i in range(1,175):
	#	Syst=abs(NominalMHT.GetBinContent(i)-genMHT.GetBinContent(i))/2.0
	#	MHTSyst.SetBinContent(i,1.0+Syst) 
	#JetIdUnc=signal_inputfile.Get(signaltag+"_jetiduncUp")
#AR-180516: addSystematicsLine(self,systype,channel,hist):
#systype=lnN, channel='sig'=signal yield histogram, hist=LumiUnc
	#print "['sig'] ", ['sig']
	#signalRegion.addSystematicsLine('lnN',['sig'],LumiUnc)
	#signalRegion.addSystematicsLine('lnN',['sig'],JetIdUnc)	
        #signalRegion.addSingleSystematic('EvtFilters','lnN',['sig'],1.05);
        #signalRegion.addSingleSystematic('JetIDUnc','lnN',['sig'],1.01);
	#signalRegion.addSystematicsLine('lnN',['sig'],TkIsoUncUp)	
	#signalRegion.addSystematicsLine('lnN',['sig'],signalSysPrefireUp)	
	#signalRegion.addSystematicsLine('lnN',['sig'],signalSysTrigSystUp)	
        #signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.027);
	#signalRegion.addSystematicsLine('lnN',['sig'],signalMCStatError);	
	
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysMisSFUp,signalSysMisSFDown)	
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysJERUp,signalSysJERDown)	
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysJECUp,signalSysJECDown)	
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysScaleUp,signalSysScaleDown)
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysISRUp,signalSysISRDown)	
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysSFUp,signalSysSFDown)	



	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalPUUp,signalPUDown)	
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],TkIsoUncUp,TkIsoUncDn)	
	##############
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysbtagCFuncUp,signalSysbtagCFuncDown)		
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysctagCFuncUp,signalSysctagCFuncDown)		
	#signalRegion.addSystematicsLineAsymShape('lnN',['sig'],signalSysmistagCFuncUp,signalSysmistagCFuncDown)		
	#Correlate HAD TAU AND LOST LEPTON SYSTEMATICS


	############
#AR-180516:CSZero and HadTauHighW as copy of LLAvgHeight_Hist
#GammaObs=DYinputfile.Get("hzvvgJNobs"), DYinputfile=ZinvHistos.root


	#QCDContamUnc=QCDInputFile.Get("PredictionContam")		
	#QCDCloseUnc=QCDInputFile.Get("PredictionClosure")		
	#QCDStatUnc=QCDInputFile.Get("PredictionStat")		
	#QCDPriorUnc=QCDInputFile.Get("PredictionPrior")		
	#QCDCoreDn=QCDInputFile.Get("PredictionCoreDown")	
	#QCDTrigDn=QCDInputFile.Get("PredictionTrigDown")	
	#QCDTrigUp=QCDInputFile.Get("PredictionTrigUp")	
	#QCDCoreUp=QCDInputFile.Get("PredictionCore")	
	#QCDTail=QCDInputFile.Get("PredictionTail")	
	#QCDUnCorrel=QCDInputFile.Get("PredictionUncorrelated")
	#for i in range(1, 175):
	#	QCDUnCorrel.GetXaxis().SetBinLabel(i, "QCDUncorrel"+CorrSigHist.GetXaxis().GetBinLabel(i))
		#CorrelLabel=CorrSigHist.GetXaxis().GetBinLabel(i).split("_")
		#print CorrelLabel
		#qcdNJetUnc.GetXaxis().SetBinLabel(i, "QCDNJetFullyCorrelated");	
		#QCDLabel="QCDCoreUnc%s_%s_%s" %(CorrelLabel[1], CorrelLabel[2], CorrelLabel[3])
		#QCDCoreUp.GetXaxis().SetBinLabel(i, QCDLabel);
		#QCDTail.GetXaxis().SetBinLabel(i, "QCDTail");
	#signalRegion.addSystematicsLine('lnN', ['qcd'], qcdNJetUnc);
	#signalRegion.addSystematicsLine('lnN',['qcd'], QCDUnCorrel);
	#signalRegion.addSystematicsLine('lnN',['qcd'], QCDTail);
        #signalRegion.addSystematicsLine('lnN',['qcd'],QCDCoreUp)

	#signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauSysMTDn)
	#signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauSysIsoDn)
	#signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauSysMuIdDn)

	#signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauEleSysIsoDn)
	#signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauEleIDSysDn)
	#signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauEleSysReco)


	#signalRegion.addSystematicsLine('lnN', ['WTop'],LLPlusHadTauTFStatUnc)
	#signalRegion.addSystematicsLine('lnN',['WTop'],LLPlusHadTauSysJECDn)
	#signalRegion.addSystematicsLine('lnN',['WTop'],LLPlusHadTauSysBMistagDn)
	#signalRegion.addSystematicsLine('lnN',['WTop'],LLPlusHadTauAccPDFSysDn)
	#signalRegion.addSystematicsLine('lnN',['WTop'],LLPlusHadTauQScaleSysDn)

	######################################################################
	######################################################################
	# 4. Write Cards
	######################################################################
	######################################################################	

	print odir, signalmu
	signalRegion.writeCards( odir );
