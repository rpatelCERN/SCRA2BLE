from ROOT import *

import os
import math
import sys
from searchRegion import *
from singleBin import *
from cardUtilities import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option("--signal", dest="signal", default = 'SMSqqqq1000',help="mass of LSP", metavar="signal")
parser.add_option("--tag", dest="tag", default = 'SinglePhoton1',help="mass of LSP", metavar="tag")
parser.add_option("--mu", dest="mu", default = 1.,help="mass of LSP", metavar="mu")
parser.add_option("--lumi", dest="lumi", default = 10.,help="mass of LSP", metavar="lumi")

parser.add_option('--qcdOnly', action='store_true', dest='qcdOnly', default=False, help='no X11 windows')
parser.add_option('--zvvOnly', action='store_true', dest='zvvOnly', default=False, help='no X11 windows')
parser.add_option('--tauOnly', action='store_true', dest='tauOnly', default=False, help='no X11 windows')
parser.add_option('--llpOnly', action='store_true', dest='llpOnly', default=False, help='no X11 windows')
parser.add_option('--allBkgs', action='store_true', dest='allBkgs', default=False, help='no X11 windows')

(options, args) = parser.parse_args()


#########################################################################################################
## to do:
## 1. put in asymmetric uncertainties from Jim/Arne(?)
## 2. add the new uncertainty scheme from Owen
## 3. try the hardcore QCD background estimate; also include lost lepton
#########################################################################################################
if __name__ == '__main__':

	sms = options.signal;
	tag = options.tag;
	lumi = float(options.lumi);
	signalmu = float(options.mu);
	odir = 'testCards-%s-%s-%s-mu%0.1f/' % ( tag,sms,str(round(lumi,1)), signalmu );
	idir = 'inputHistograms/histograms_%sfb/' % ( str(int(lumi)) );
	if os.path.exists(odir): os.system( "rm -r %s" % (odir) );
	os.makedirs(odir);

	print odir, signalmu

	#------------------------------------------------------------------------------------------------
	## 1. Fill Rates for each signal region

	# histogram gymnastics...
	signalRegion_file = TFile(idir+"/RA2bin_signal.root");
	data_file= TFile(idir+"/RA2bin_Data%spb.root" %(str(int(lumi))));
	Data_Hist=data_file.Get("RA2bin_data")
	Data_List=binsToList(Data_Hist);
	signalSFB_file =TFile(idir+"/RA2bin_signalSF.root");
	signalSysSFUp_file=TFile("inputSignalSys/RA2bin_signal_btagSFuncUp.root");
	signalSysSFDown_file=TFile("inputSignalSys/RA2bin_signal_btagSFuncDown.root");
	signalSysMisSFUp_file=TFile("inputSignalSys/RA2bin_signal_mistagSFuncUp.root");
	signalSysMisSFDown_file=TFile("inputSignalSys/RA2bin_signal_mistagSFuncDown.root");

	sphotonRegion_file = TFile(idir+"/RA2bin_GJet_CleanVars.root");
	lowdphiRegion_file = TFile(idir+"/RA2bin_LDP.root");
		
	# signal --------
	signalRegion_sigHist = signalSFB_file.Get("RA2bin_"+sms);
	signalRegion_sigHistSFUp= signalSysSFUp_file.Get("RA2bin_"+sms);
	signalRegion_sigHistSFDown= signalSysSFDown_file.Get("RA2bin_"+sms);
	signalRegion_sigHistMisSFUp = signalSysMisSFUp_file.Get("RA2bin_"+sms)
	signalRegion_sigHistMisSFDown = signalSysMisSFDown_file.Get("RA2bin_"+sms)
	signalRegion_sigHist.Scale(lumi/3000.);
	signalRegion_sigHistSFUp.Scale(lumi/3000.);
	signalRegion_sigHistSFDown.Scale(lumi/3000.);
	signalRegion_sigHistMisSFUp.Scale(lumi/3000.);
	signalRegion_sigHistMisSFDown.Scale(lumi/3000.);
	
	tagsForSignalRegion = binLabelsToList(signalRegion_sigHist);
	signalRegion_sigList = binsToList( signalRegion_sigHist );
	signalRegion_sigListSFUp=binsToList( signalRegion_sigHistSFUp );
	signalRegion_sigListSFDown=binsToList( signalRegion_sigHistSFDown );
	signalRegion_sigListMisSFUp=binsToList( signalRegion_sigHistMisSFUp );
	signalRegion_sigListMisSFDown=binsToList( signalRegion_sigHistMisSFDown );
	# zinv --------
	# zinv_sr = signalRegion_file.Get("RA2bin_Zinv");
	# gjet_cr = sphotonRegion_file.Get("RA2bin_GJet");
	# h_newZinvSRYields = hutil_clone0BtoNB( zinv_sr );
	# signalRegion_zvvList = binsToList( h_newZinvSRYields );
	DYinputfile = TFile("inputsZinv/DYhistos.root")
	signalRegion_zvvRatesFromDY = DYinputfile.Get("DYvalue")
	signalRegion_zvvList = binsToList( signalRegion_zvvRatesFromDY );

	# ll --------
	LL_file = TFile("inputsLostLepton/LLPrediction_Oct15_2.root" );
	LLPrediction_Hist=LL_file.Get("Prediction_data/totalPred_LL");
	LLCS_Hist=LL_file.Get("Prediction_data/totalCS_LL");
	LLWeight_Hist=LL_file.Get("Prediction_data/avgWeight_LL");
	LLMCWeight_Hist=LL_file.Get("Prediction_MC/avgWeight_LL_MC");
	
	#systematics
	LLSysIsoTrackUp_Hist=LL_file.Get("Prediction_data/totalPredIsoTrackSysUp_LL")
	LLSysIsoTrackDown_Hist=LL_file.Get("Prediction_data/totalPredIsoTrackSysDown_LL")
	LLSysMTUp_Hist=LL_file.Get("Prediction_data/totalPredMTWSysUp_LL");
	LLSysMTDown_Hist=LL_file.Get("Prediction_data/totalPredMTWSysDown_LL");
	LLSysPurUp_Hist=LL_file.Get("Prediction_data/totalPredPuritySysUp_LL");	
	LLSysPurDown_Hist=LL_file.Get("Prediction_data/totalPredPuritySysDown_LL");
	LLSysSinglePurUp_Hist=LL_file.Get("Prediction_data/totalPredSingleLepPuritySysUp_LL");
	LLSysSinglePurDown_Hist=LL_file.Get("Prediction_data/totalPredSingleLepPuritySysDown_LL");
	LLSysDiLepPurUp_Hist=LL_file.Get("Prediction_data/totalPredDiLepFoundSysUp_LL")
	LLSysDiLepPurDown_Hist=LL_file.Get("Prediction_data/totalPredDiLepFoundSysDown_LL")
	LLSysMuIsoUp_Hist=LL_file.Get("Prediction_data/totalPredMuIsoSysUp_LL");
	LLSysMuIsoDown_Hist=LL_file.Get("Prediction_data/totalPredMuIsoSysDown_LL");
	LLSysMuRecoUp_Hist=LL_file.Get("Prediction_data/totalPredMuRecoSysUp_LL");
	LLSysMuRecoDown_Hist=LL_file.Get("Prediction_data/totalPredMuRecoSysDown_LL")
	LLSysMuAccUp_Hist=LL_file.Get("Prediction_data/totalPredMuAccSysUp_LL");
	LLSysMuAccDown_Hist=LL_file.Get("Prediction_data/totalPredMuAccSysDown_LL")
	LLSysElecIsoUp_Hist=LL_file.Get("Prediction_data/totalPredElecIsoSysUp_LL");
	LLSysElecIsoDown_Hist=LL_file.Get("Prediction_data/totalPredElecIsoSysDown_LL");
	LLSysElecRecoUp_Hist=LL_file.Get("Prediction_data/totalPredElecRecoSysUp_LL");
	LLSysElecRecoDown_Hist=LL_file.Get("Prediction_data/totalPredElecRecoSysDown_LL")
	LLSysElecAccUp_Hist=LL_file.Get("Prediction_data/totalPredElecAccSysUp_LL");
	LLSysElecAccDown_Hist=LL_file.Get("Prediction_data/totalPredElecAccSysDown_LL")
	LLSysNCUp_Hist=LL_file.Get("Prediction_data/totalPredNonClosureUp_LL")
	LLSysNCDown_Hist=LL_file.Get("Prediction_data/totalPredNonClosureDown_LL")


	signalRegion_LLList = binsToList( LLPrediction_Hist );
	signalRegion_WeightList=binsToList(LLWeight_Hist);
	signalRegion_MCWeightList=binsToList(LLMCWeight_Hist);
	signalRegion_CSList=binsToList(LLCS_Hist)
	LLSysIsoTrackUp=binsToList(LLSysIsoTrackUp_Hist)
	LLSysIsoTrackDown=binsToList(LLSysIsoTrackDown_Hist)
	LLSysMTUp=binsToList(LLSysMTUp_Hist)	
	LLSysMTDown=binsToList(LLSysMTDown_Hist)	
	LLSysPurUp=binsToList(LLSysPurUp_Hist)
	LLSysPurDown=binsToList(LLSysPurDown_Hist)
	LLSysSinglePurUp=binsToList(LLSysSinglePurUp_Hist)
	LLSysSinglePurDown=binsToList(LLSysSinglePurDown_Hist)
	LLSysPurDown=binsToList(LLSysSinglePurDown_Hist)
	LLSysDiLepPurUp=binsToList(LLSysDiLepPurUp_Hist)
	LLSysDiLepPurDown=binsToList(LLSysDiLepPurDown_Hist)
	LLSysMuIsoUp=binsToList(LLSysMuIsoUp_Hist)
	LLSysMuIsoDown=binsToList(LLSysMuIsoDown_Hist)
	LLSysMuRecoUp=binsToList(LLSysMuRecoUp_Hist)
	LLSysMuRecoDown=binsToList(LLSysMuRecoDown_Hist)
	LLSysMuAccUp=binsToList(LLSysMuAccUp_Hist)
	LLSysMuAccDown=binsToList(LLSysMuAccDown_Hist)
	LLSysElecIsoUp=binsToList(LLSysElecIsoUp_Hist)
	LLSysElecIsoDown=binsToList(LLSysElecIsoDown_Hist)
	LLSysElecRecoUp=binsToList(LLSysElecRecoUp_Hist)
	LLSysElecRecoDown=binsToList(LLSysElecRecoDown_Hist)
	LLSysElecAccUp=binsToList(LLSysElecAccUp_Hist)
	LLSysElecAccDown=binsToList(LLSysElecAccDown_Hist)
	LLSysNCUp=binsToList(LLSysNCUp_Hist)
	LLSysNCDown=binsToList(LLSysNCDown_Hist)
	for i in range(len(LLSysNCUp)):
		if(LLSysMTUp[i]<-99 or signalRegion_CSList[i]<2): LLSysMTUp[i]=1.0;
		if(LLSysMTDown[i]<-99 or signalRegion_CSList[i]<2 ): LLSysMTDown[i]=1.0;
		if(LLSysIsoTrackUp[i]<-99 or signalRegion_CSList[i]<2):LLSysIsoTrackUp[i]=1.0
		if(LLSysIsoTrackDown[i]<-99 or signalRegion_CSList[i]<2):LLSysIsoTrackDown[i]=1.0
		if(LLSysPurUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysPurUp[i]=1.0;
		if(LLSysPurDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysPurDown[i]=1.0;
		if(LLSysSinglePurUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysSinglePurUp[i]=1.0;
		if(LLSysSinglePurDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysSinglePurDown[i]=1.0;
		if(LLSysDiLepPurUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysDiLepPurUp[i]=1.0;
		if(LLSysDiLepPurDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysDiLepPurDown[i]=1.0;
		if(LLSysMuIsoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuIsoUp[i]=1.0;
		if(LLSysMuIsoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuIsoDown[i]=1.0;
		if(LLSysMuRecoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuRecoUp[i]=1.0;
		if(LLSysMuRecoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuRecoDown[i]=1.0;
		if(LLSysMuAccUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuAccUp[i]=1.0;
		if(LLSysMuAccDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuAccDown[i]=1.0;

		if(LLSysElecIsoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecIsoUp[i]=1.0;
		if(LLSysElecIsoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecIsoDown[i]=1.0;
		if(LLSysElecRecoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecRecoUp[i]=1.0;
		if(LLSysElecRecoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecRecoDown[i]=1.0;
		if(LLSysElecAccUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecAccUp[i]=1.0;
		if(LLSysElecAccDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecAccDown[i]=1.0;
	#Also Get Sumw2 errors
	LLSumW2errors=[]
	for i in range(1,LLPrediction_Hist.GetNbinsX()+1):
		if(LLPrediction_Hist.GetBinError(i)>0.000000001):
			multError=LLPrediction_Hist.GetBinError(i)/(LLPrediction_Hist.GetBinContent(i))
			LLSumW2errors.append(1.0+multError);
		else: LLSumW2errors.append(1.0)

	
	HadTau_file = TFile("inputsHadTau/HadTauInputs%spb.root" % (str(int(lumi)) ));
	
	HadTauPrediction_Hist=HadTau_file.Get("searchBin_nominal")
	HadTauSqrtSumw2_Hist=HadTau_file.Get("SqrtSumW2")
	HadTauBMistagUp_Hist=HadTau_file.Get("searchBin_BMistagUp")	
	HadTauBMistagDown_Hist=HadTau_file.Get("searchBin_BMistagDn")
	HadTauSysNCJet0_Hist=HadTau_file.Get("searchBin_ClosureNj46")
	HadTauSysNCJet1_Hist=HadTau_file.Get("searchBin_ClosureNj78")	
	HadTauSysNCJet2_Hist=HadTau_file.Get("searchBin_ClosureNj9")	
	HadTauSysNCWjetsMHT2_Hist=HadTau_file.Get("searchBin_ClosureMHT2Wjets")	
	HadTauSysNCTTbarMHT2_Hist=HadTau_file.Get("searchBin_ClosureMHT2TTbar")	
	HadTauSysNCWjetsMHT3_Hist=HadTau_file.Get("searchBin_ClosureMHT3Wjets")	
	HadTauSysNCTTbarMHT3_Hist=HadTau_file.Get("searchBin_ClosureMHT3TTbar")
	HadTauSysUncCorrections_Hist=HadTau_file.Get("searchBin_UncertaintyCorrectionStats")
	
	signalRegion_tauList=binsToList(HadTauPrediction_Hist)
	tauBMistagUp=binsToList(HadTauBMistagUp_Hist)
	tauBMistagDown=binsToList(HadTauBMistagDown_Hist)
	tauNonClosureJet0=binsToList(HadTauSysNCJet0_Hist)
	tauNonClosureJet1=binsToList(HadTauSysNCJet1_Hist)       	
	tauNonClosureJet2=binsToList(HadTauSysNCJet2_Hist)
	tauNonClosureWJMHT2=binsToList(HadTauSysNCWjetsMHT2_Hist)
	tauNonClosureTTbarMHT2=binsToList(HadTauSysNCTTbarMHT2_Hist)
	tauNonClosureWJMHT3=binsToList(HadTauSysNCWjetsMHT3_Hist)
	tauNonClosureTTbarMHT3=binsToList(HadTauSysNCTTbarMHT3_Hist)
	tauSqrtSumW2=binsToList(HadTauSqrtSumw2_Hist)
	tauUncCorr=binsToList(HadTauSysUncCorrections_Hist)
	# print  "./inputsLostLepton/statunc%sfb.txt" % (str(int(lumi)))
	
	#signalRegion_statUncList = textToList( "./inputsLostLepton/statunc%sfb.txt" % (str(int(lumi))), 0 );
	#signalRegion_sysUncList = textToList( "./inputsLostLepton/sysunc%sfb.txt" % (str(int(lumi))), 0 );

	# had tau
#	signalRegion_tauList = textToList( "inputsHadTau/HadTauMCPred%sfb.txt" % (str(int(lumi))), 0 );
	
	#hadtauSystematics = textToList( "inputsHadTau/HadTauSumw2.txt", 0 )
	#controlRegion_tauList = textToList( "inputsHadTau/TauControlBins%sfb.txt" % (str(int(lumi))), 0 );
	#for i in range(len(controlRegion_tauList)):
	#	if(controlRegion_tauList[i]<2):print controlRegion_tauList[i]
	
	# QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ
	# QCD stuff
	# low dphi region stuff

	ratesForSignalRegion_QCDList = [];
	NSRForSignalRegion_QCDList = textToList("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),6);
	#print NSRForSignalRegion_QCDList
	ratesForLowdphiRegion_QCDList = [];
	NCRForLowdphiRegion_QCDList = textToList("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),2);
	obsForLowdphiRegion_QCDList = [];
	ratiosForLowdphiRegion = textToList("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),5);
	ContaminForLowdphiRegion = textToList("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),3);
	lowdphiRegion_sigHist = lowdphiRegion_file.Get("RA2bin_"+sms);
	ratesForLowdphiRegion_sigList = binsToList(lowdphiRegion_sigHist);
	tagsForLowDPhiRegion = binLabelsToList(lowdphiRegion_sigHist)

	lowdphiRegion_sigHist = lowdphiRegion_file.Get("RA2bin_"+sms);
	ratesForLowdphiRegion_sigList = binsToList(lowdphiRegion_sigHist);
	tagsForLowDPhiRegion = binLabelsToList(lowdphiRegion_sigHist)
	QCDcontributionsPerBin = [];
	for i in range(len(tagsForLowDPhiRegion)): 
		QCDcontributionsPerBin.append( [ 'sig','qcd','contam' ] );
		if(NCRForLowdphiRegion_QCDList[i]>0.0):
			#BkgRateSubtracted=NCRForLowdphiRegion_QCDList[i]-ContaminForLowdphiRegion[i]
			BkgRateSubtracted=NCRForLowdphiRegion_QCDList[i]
			if BkgRateSubtracted>0:
				ratesForLowdphiRegion_QCDList.append(BkgRateSubtracted)
				ratesForSignalRegion_QCDList.append(BkgRateSubtracted *ratiosForLowdphiRegion[i])			
			else:
				ratesForLowdphiRegion_QCDList.append(1.0)
				ratesForSignalRegion_QCDList.append(ratiosForLowdphiRegion[i]);
		else:
			ratesForLowdphiRegion_QCDList.append(1.0)
			ratesForSignalRegion_QCDList.append(ratiosForLowdphiRegion[i]);
		obsForLowdphiRegion_QCDList.append( NCRForLowdphiRegion_QCDList[i] );

	LowdphiControlRegion = searchRegion('Lowdphi', QCDcontributionsPerBin, tagsForLowDPhiRegion);	
	qcdcontrolRegion_Rates = [];
	qcdcontrollRegion_Observed = [];
	for i in range(LowdphiControlRegion._nBins):
		curobsC = 0;
		curobsC += obsForLowdphiRegion_QCDList[i]
		currateC = [];
		currateC.append( 0. );
		currateC.append( ratesForLowdphiRegion_QCDList[i] );
		currateC.append( ContaminForLowdphiRegion[i] );	
		#currateC.append(0.0)
		qcdcontrolRegion_Rates.append(currateC);
		qcdcontrollRegion_Observed.append(curobsC);	

	LowdphiControlRegion.fillRates(qcdcontrolRegion_Rates);
	LowdphiControlRegion.setObservedManually(qcdcontrollRegion_Observed);
	LowdphiControlRegion.writeRates();

	# QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ

	# photon region

	#sphoton observeds
	sphotonObserved = [194,45,14,17,4,2,11,3,1,0,0,0,0,0,1,0,0,0]; # thess eventually will be histograms
	RzgVals = [0.418,0.419,0.430,0.491,0.534,0.494,0.378,0.468,0.420,0.595,0.512,0.464,0.484,0.469,0.361,0.165,0.687,0.824];
	RzgErrsAbs = [0.005,0.007,0.013,0.014,0.041,0.028,0.038,0.027,0.035,0.094,0.107,0.115,0.202,0.095,0.075,0.100,0.434,0.890];
	PurVals = [0.790,0.823,0.808,0.833,0.874,0.759,0.790,0.721,0.874,0.759,0.759,0.759,0.759,0.759,0.874,0.759,0.759,0.759];	
	PurErrsAbs = [0.047,0.050,0.049,0.052,0.058,0.045,0.047,0.045,0.058,0.045,0.045,0.045,0.045,0.045,0.058,0.045,0.045,0.045];
	RzgErrs = [];
	PurErrs = [];
	for i in range(len(RzgVals)): RzgErrs.append( RzgErrsAbs[i]/RzgVals[i] );
	for i in range(len(PurVals)): PurErrs.append( PurErrsAbs[i]/PurVals[i] );
	PhoRatios = [];
	doubleRatioCentralValue = 0.94;
	for i in range(len(RzgVals)): PhoRatios.append( 1./RzgVals[i]/PurVals[i]/doubleRatioCentralValue );

	phoRegion_sigHist = sphotonRegion_file.Get("RA2bin_"+sms)
	tagsForSinglePhoton = binLabelsToList(phoRegion_sigHist)
	contributionsPerBin = [];
	for i in range(len(tagsForSinglePhoton)): contributionsPerBin.append(['sig','zvv']);
	sphotonRegion = searchRegion('sphoton', contributionsPerBin, tagsForSinglePhoton);              
	phoRegion_sigList = binsToList(phoRegion_sigHist);
	phoRegion_Rates = [];
	for i in range(sphotonRegion._nBins):
			tmpList = [];
			#tmpList.append(phoRegion_sigList[i]);
			tmpList.append(0.000001);
			if sphotonObserved[i] > 0: tmpList.append(sphotonObserved[i]);
			else: tmpList.append(PhoRatios[i]);
			phoRegion_Rates.append( tmpList );
	sphotonRegion.fillRates( phoRegion_Rates );
	sphotonRegion.setObservedManually(sphotonObserved);
   #compute the Zvv actual yields to be put in the observed lines
	sphotonObservedExt = [];
	RzgValsExt = [];
	PurValsExt = [];
	for i in range(4):
			sphotonObservedExt.extend(sphotonObserved[0:6]); RzgValsExt.extend(RzgVals[0:6]); PurValsExt.extend(PurVals[0:6])
	for i in range(4):
			sphotonObservedExt.extend(sphotonObserved[6:12]); RzgValsExt.extend(RzgVals[6:12]); PurValsExt.extend(PurVals[6:12])
	for i in range(4):
			sphotonObservedExt.extend(sphotonObserved[12:18]); RzgValsExt.extend(RzgVals[12:18]); PurValsExt.extend(PurVals[12:18])

	ZvvYieldsInSignalRegion = [sphotonObservedExt[i]*RzgValsExt[i]*PurValsExt[i]*signalRegion_zvvList[i] for i in range(len(sphotonObservedExt))]
	ZvvRatesInSignalRegion = [];
	for i in range(len(sphotonObservedExt)):
			if sphotonObservedExt[i] > 0: ZvvRatesInSignalRegion.append( ZvvYieldsInSignalRegion[i] );
			else: ZvvRatesInSignalRegion.append(signalRegion_zvvList[i]);

	#print ZvvYieldsInSignalRegion

	# QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ
	# accounting for LL Region
	tagsForSLControlRegion=[]	
	tagsForHadControlRegion=[]
	SLcontrolContributionsPerBin = [];
	addControl=[]
	for i in range(len(tagsForSignalRegion)): 
		#if(signalRegion_CSList[i]<2):
		tmpcontributionsSL = [];
		tmpcontributionsSL.append( 'sig' );
		if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly): tmpcontributionsSL.append( 'WTopSL' );
		if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly): tmpcontributionsSL.append( 'WTopSLHighW' );
		if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpcontributionsSL.append( 'WTopHad' );
		if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpcontributionsSL.append( 'WTopHadHighW' );			
		if options.llpOnly and signalRegion_CSList[i]<2  and not (options.tauOnly and  options.llpOnly):
			addControl.append(i);
			SLcontrolContributionsPerBin.append( tmpcontributionsSL );
			tagsForSLControlRegion.append(tagsForSignalRegion[i]);
		if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly):
			addControl.append(i); 
			SLcontrolContributionsPerBin.append( tmpcontributionsSL );
			tagsForSLControlRegion.append(tagsForSignalRegion[i]);			
	SLcontrolRegion = searchRegion('SLControl', SLcontrolContributionsPerBin, tagsForSLControlRegion)
	SLcontrolRegion_Obs = [];
	SLcontrolRegion_Rates = [];
	HadcontrolRegion_Obs = [];
	HadcontrolRegion_Rates = [];
	for i in range(len(addControl)):
		tmpList=[]
		tmpList.append(0);
		if options.llpOnly and not options.tauOnly and not options.allBkgs: 
				tmpList.append(0.);			
				if(signalRegion_CSList[i]<=1): tmpList.append(1.0); 
				else: tmpList.append(0.0); 
		if options.allBkgs or (options.tauOnly and options.llpOnly):
				tmpList.append(0.);
				tmpList.append(0.0);
		if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpList.append(0.0);
		if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpList.append(1.);
		SLcontrolRegion_Obs.append(0.0);
		SLcontrolRegion_Rates.append(tmpList);
	#print len(SLcontrolRegion_Rates), len(SLcontrolRegion_Obs)
	SLcontrolRegion.fillRates(SLcontrolRegion_Rates);
	SLcontrolRegion.setObservedManually(SLcontrolRegion_Obs);
	# -------------------------------
	# signal region
	contributionsPerBin = [];
	for i in range(len(tagsForSignalRegion)): 
		tmpcontributions = [];
		tmpcontributions.append('sig');
		if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly): tmpcontributions.append('WTopSL');
		if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly): tmpcontributions.append('WTopSLHighW');
		if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpcontributions.append('WTopHad');
		if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpcontributions.append('WTopHadHighW');
		if options.allBkgs or options.zvvOnly: tmpcontributions.append('zvv');
		if options.allBkgs or options.qcdOnly: tmpcontributions.append('qcd');
		contributionsPerBin.append(tmpcontributions);

	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)

	signalRegion_Rates = [];
	signalRegion_Obs = [];
	controlRegion_Rates=[];

	for i in range(signalRegion._nBins):
		srobs = Data_List[i];
		srobs = 0;
		srobs += signalRegion_sigList[i]*signalmu;
		#if options.allBkgs or options.qcdOnly: srobs += NCRForLowdphiRegion_QCDList[i]*ratiosForLowdphiRegion[i]
		if options.allBkgs or options.qcdOnly: srobs += NSRForSignalRegion_QCDList[i];
		if options.allBkgs or options.zvvOnly: srobs += ZvvYieldsInSignalRegion[i];
		if options.allBkgs or options.llpOnly: srobs += signalRegion_LLList[i];
		if options.allBkgs or options.tauOnly: srobs += signalRegion_tauList[i];
		signalRegion_Obs.append( srobs );

		tmpList = [];
		tmpList.append(signalRegion_sigList[i]);

		# LL rate
		
		if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly):		
			# addControl=[]	
			#if(signalRegion_CSList[i]>=2):
			tmpList.append(signalRegion_LLList[i]);
			#else:
			#tmpList.append(0.0)
			if(signalRegion_CSList[i]>=2):
				tmpList.append(0.0)
			if(signalRegion_CSList[i]==1):
				tmpList.append(signalRegion_MCWeightList[i]*3.0)
			if(signalRegion_CSList[i]<1):
				tmpList.append(signalRegion_MCWeightList[i]*3.0)
		# Had Tau rate
		if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): 
				tmpList.append(signalRegion_tauList[i])
				tmpList.append(0.25);
		if options.allBkgs or options.zvvOnly: tmpList.append( ZvvRatesInSignalRegion[i]) ;
		if options.allBkgs or options.qcdOnly: tmpList.append( ratesForSignalRegion_QCDList[i] );
		signalRegion_Rates.append( tmpList );
	
	signalRegion.fillRates( signalRegion_Rates );
	signalRegion.setObservedManually(signalRegion_Obs)

	SLcontrolRegion.writeRates();
	sphotonRegion.writeRates();
	signalRegion.writeRates();

	# #------------------------------------------------------------------------------------------------
	# #------------------------------------------------------------------------------------------------
	# #------------------------------------------------------------------------------------------------
	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	# ['SMSqqqq1000','SMSqqqq1400','SMStttt1200','SMStttt1500','SMSbbbb1000','SMSbbbb1500']
	pdf=1.3
	ISR=1.01
	if(sms=='SMSqqqq1400' or sms=='SMStttt1200' or sms=='SMSbbbb1000'):
		ISR=1.08
		pdf=1.10
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);
	signalRegion.addSingleSystematic('EvtFilters','lnN',['sig'],1.03);
	signalRegion.addSingleSystematic('PUwUnc','lnN',['sig'],1.03);
	signalRegion.addSingleSystematic('TrigEff','lnN',['sig'],1.02);
	signalRegion.addSingleSystematic('ISR','lnN',['sig'],ISR);
	signalRegion.addSingleSystematic('pdf','lnN',['sig'],pdf);
	signalRegion.addSingleSystematic('UnclEUnc', 'lnN', ['sig'], 1.01);
	signalRegion.addSingleSystematic('JERUnc', 'lnN', ['sig'], 1.02);

	for i in range(signalRegion.GetNbins()):
		if( signalRegion_sigList[i]>0.000001):
			signalRegion.addAsymSystematic('MisTagSFunc', 'lnN', ['sig'], signalRegion_sigListMisSFUp[i]/signalRegion_sigList[i], signalRegion_sigListMisSFDown[i]/signalRegion_sigList[i], '', i)
			signalRegion.addAsymSystematic('BTagSFUnc','lnN', ['sig'], (signalRegion_sigListSFUp[i]/signalRegion_sigList[i]),signalRegion_sigListSFDown[i]/signalRegion_sigList[i],'', i)
	#signalRegion.addSingleSystematic('BTagSFUnc', 'lnN', ['sig'], 1.15, 'BTags0')	
	#signalRegion.addSingleSystematic('BTagSFUnc', 'lnN', ['sig'], 1.0, 'BTags1')
	#signalRegion.addSingleSystematic('BTagSFUnc', 'lnN', ['sig'], 1.0, 'BTags2')
	#signalRegion.addSingleSystematic('BTagSFUnc', 'lnN', ['sig'], 0.95, 'BTags3')

	signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 1.0, 'MHT0_HT0');
	signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 0.95, 'MHT0_HT1');
	signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 1.1, 'MHT0_HT2');
	signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 0.95, 'MHT1_HT3');
	signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 0.95, 'MHT1_HT4');
	signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 1.1, 'MHT2_HT5');

	### Zvv uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.zvvOnly:

		# connect the single photon CR to the signal region
		singlePhotonBins = ["NJets0_BTags._MHT0_HT0","NJets0_BTags._MHT0_HT1","NJets0_BTags._MHT0_HT2","NJets0_BTags._MHT1_HT3","NJets0_BTags._MHT1_HT4","NJets0_BTags._MHT2_HT5",
							"NJets1_BTags._MHT0_HT0","NJets1_BTags._MHT0_HT1","NJets1_BTags._MHT0_HT2","NJets1_BTags._MHT1_HT3","NJets1_BTags._MHT1_HT4","NJets1_BTags._MHT2_HT5",
							"NJets2_BTags._MHT0_HT0","NJets2_BTags._MHT0_HT1","NJets2_BTags._MHT0_HT2","NJets2_BTags._MHT1_HT3","NJets2_BTags._MHT1_HT4","NJets2_BTags._MHT2_HT5"];
		for i in range(len(singlePhotonBins)):
			signalRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);
			sphotonRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);

		# added to all bins (photon efficiency)
		#print len(RzgErrs),len(PurErrs)
		sphotonRegion.addSystematicFromList('PhoRzgUnc','lnN',['zvv'],RzgErrs);	
		sphotonRegion.addSystematicFromList('PhoEffUnc','lnN',['zvv'],PurErrs);	
		## RZg double ratio from Jim H.
		sphotonRegion.addAsymSystematic('PhoRZgDblRatio','lnN',['zvv'],1.33,1.26,'NJets'); # adjusted to make relative

		## all the Drell-Yan systematics now nicely wrapped up in a bow
		signalRegion.addSystematicFromList('DYstat','lnN',['zvv'], binsToList(DYinputfile.Get("DYstat")));
		signalRegion.addSystematicFromList('DYsysKin','lnN',['zvv'], binsToList(DYinputfile.Get("DYsysKin")));
		signalRegion.addAsymSystematicFromList('DYsysNj','lnN',['zvv'], binsToList(DYinputfile.Get("DYsysNjUp")), binsToList(DYinputfile.Get("DYsysNjDown")));


	### LL uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly):
		for i in range(signalRegion.GetNbins()):
			if(signalRegion_CSList[i]>2):
				signalRegion.addAsymSystematic("LLNonClos"+tagsForSignalRegion[i],'lnN',['WTopSL'],(LLSysNCUp[i]), (LLSysNCDown[i]),'', i)
				signalRegion.addAsymSystematic("LLMuIso",'lnN',['WTopSL'],(LLSysMuIsoUp[i]), (LLSysMuIsoDown[i]),'', i)
				signalRegion.addAsymSystematic("LLMuReco",'lnN',['WTopSL'],(LLSysMuRecoUp[i]), (LLSysMuRecoDown[i]),'', i)
				signalRegion.addAsymSystematic("LLEleIso",'lnN',['WTopSL'],(LLSysElecIsoUp[i]), (LLSysElecIsoDown[i]),'', i)
				signalRegion.addAsymSystematic("LLEleReco",'lnN',['WTopSL'],(LLSysElecRecoUp[i]), (LLSysElecRecoDown[i]),'', i)	
			if(signalRegion_CSList[i]==1):
				signalRegion.addSingleSystematic('LLavgWUnc'+tagsForSignalRegion[i],'lnN',['WTopSLHighW'], 2.0,'',i); 
		signalRegion.addAsymSystematic("LLMTW_NJet0",'lnN',['WTopSL'],LLSysMTUp, LLSysMTDown,'NJets0')
		signalRegion.addAsymSystematic("LLMTW_NJet1",'lnN',['WTopSL'],LLSysMTUp, LLSysMTDown,'NJets1')
		signalRegion.addAsymSystematic("LLMTW_NJet2",'lnN',['WTopSL'],LLSysMTUp, LLSysMTDown,'NJets2')
		
	
		signalRegion.addAsymSystematic("LLSingleLepPurity_NJet0",'lnN',['WTopSL'],LLSysPurUp, LLSysPurDown,'NJets0')
		signalRegion.addAsymSystematic("LLSingleLepPurity_NJet1",'lnN',['WTopSL'],LLSysPurUp, LLSysPurDown,'NJets1')
		signalRegion.addAsymSystematic("LLSingleLepPurity_NJet2",'lnN',['WTopSL'],LLSysPurUp, LLSysPurDown,'NJets2')
		
		signalRegion.addAsymSystematic("LLDiLepPurity_NJet0",'lnN',['WTopSL'],LLSysDiLepPurUp, LLSysDiLepPurDown,'NJets0')
		signalRegion.addAsymSystematic("LLDiLepPurity_NJet1",'lnN',['WTopSL'],LLSysDiLepPurUp, LLSysDiLepPurDown,'NJets1')
		signalRegion.addAsymSystematic("LLDiLepPurity_NJet2",'lnN',['WTopSL'],LLSysDiLepPurUp, LLSysDiLepPurDown,'NJets2')
	
		
		NJbinsLL=['NJets1', 'NJets2']
		MHTHTBinsLL=['MHT0_HT0','MHT0_HT1','MHT0_HT2', 'MHT1_HT3','MHT1_HT4','MHT2_HT5']
		for h in range(len(MHTHTBinsLL)):
			signalRegion.addAsymSystematic("LLIsoTrackNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysIsoTrackUp), (LLSysIsoTrackDown),'NJets0_BTags._'+str(MHTHTBinsLL[h]))
			signalRegion.addAsymSystematic("MuAccNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysMuAccUp), (LLSysMuAccDown),'NJets0_BTags._'+str(MHTHTBinsLL[h]))
			signalRegion.addAsymSystematic("ElecAccNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysElecAccUp), (LLSysElecAccDown),'NJets0_BTags._'+str(MHTHTBinsLL[h]))
			
		for j in range(len(NJbinsLL)): print NJbinsLL[j]
		for h in range(len(MHTHTBinsLL)):	
			signalRegion.addAsymSystematic("LLIsoTrack7Jets"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysIsoTrackUp), (LLSysIsoTrackDown),str(NJbinsLL[j])+"_BTags._"+str(MHTHTBinsLL[h]))
			signalRegion.addAsymSystematic("MuAccN7Jets_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysMuAccUp), (LLSysMuAccDown),str(NJbinsLL[j])+'_BTags._'+str(MHTHTBinsLL[h]))
			signalRegion.addAsymSystematic("ElecAccN7Jets_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysElecAccUp), (LLSysElecAccDown),str(NJbinsLL[j])+'_BTags._'+str(MHTHTBinsLL[h]))

		NJbinsLLPur=['NJets0', 'NJets1', 'NJets2']
		MHTBins=['MHT0', 'MHT1', 'MHT2']
		for j in range(len(NJbinsLLPur)):
			for m in range(len(MHTBins)):
			   signalRegion.addAsymSystematic("LLPurity_"+str(MHTBins[m])+"_"+str(NJbinsLLPur[j]),'lnN',['WTopSL'],LLSysPurUp,LLSysPurDown,str(NJbinsLLPur[j])+"_BTags._"+str(MHTBins[m])+"_HT.")
	
	if options.allBkgs or options.tauOnly or options.llpOnly or (options.tauOnly and  options.llpOnly):
		for i in range(signalRegion.GetNbins()):
			if(signalRegion_CSList[i]<2):
				if options.allBkgs or (options.tauOnly and  options.llpOnly): 
					#signalRegion.addSingleSystematic('LLSCSR'+tagsForSignalRegion[i],'lnU',['WTopSLHighW'],100,'',i);
					signalRegion.addSingleSystematic('TAUSCSR'+tagsForSignalRegion[i],'lnU',['WTopHadHighW','WTopSLHighW'],100,'',i);
				if options.tauOnly and not (options.tauOnly and  options.llpOnly): signalRegion.addSingleSystematic('LLSCSR'+tagsForSignalRegion[i],'lnU',['WTopHadHighW'],100,'',i);
				if options.llpOnly and not (options.tauOnly and  options.llpOnly): signalRegion.addSingleSystematic('LLSCSR'+tagsForSignalRegion[i],'lnU',['WTopSLHighW'],100,'',i);
			else: 
				if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): signalRegion.addSingleSystematic('TAUSCSR'+tagsForSignalRegion[i],'lnU',['WTopHadHighW'],100,'',i);
				if options.allBkgs: 
					signalRegion.addCorrelSystematic('LLHadTauCorrelError'+tagsForSignalRegion[i], 'lnN', ['WTopSL','WTopHad'], LLSumW2errors[i], 1+(tauSqrtSumW2[i]/signalRegion_tauList[i]), '',i)			
				if options.llpOnly and not (options.tauOnly and  options.llpOnly):
					signalRegion.addSingleSystematic('LLSumWError'+tagsForSignalRegion[i], 'lnN', ['WTopSL'], LLSumW2errors[i], '',i)		

		for i in range(SLcontrolRegion.GetNbins()):
			if options.allBkgs or (options.tauOnly and  options.llpOnly): 
				if(signalRegion_CSList[i]<2): 
					#SLcontrolRegion.addSingleSystematic('LLSCSR'+tagsForSLControlRegion[i],'lnU',['WTopSLHighW'],100,'',i);
					SLcontrolRegion.addSingleSystematic('TAUSCSR'+tagsForSLControlRegion[i],'lnU',['WTopHadHighW'],100,'',i);
				else: SLcontrolRegion.addSingleSystematic('TAUSCSR'+tagsForSLControlRegion[i],'lnU',['WTopHadHighW'],100,'',i);
			if options.tauOnly and not (options.tauOnly and  options.llpOnly):
				SLcontrolRegion.addSingleSystematic('LLSCSR'+tagsForSLControlRegion[i],'lnU',['WTopHadHighW'],100,'',i);
			if options.llpOnly and not (options.tauOnly and  options.llpOnly):
				SLcontrolRegion.addSingleSystematic('LLSCSR'+tagsForSLControlRegion[i],'lnU',['WTopSLHighW'],100,'',i);		

	### hadtau uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly):
		for i in range(signalRegion.GetNbins()):
			njetTag = tagsForSignalRegion[i].split('_')[0];
			tauNonClosureJet0[i]=1.0+tauNonClosureJet0[i];
			tauNonClosureJet1[i]=1.0+tauNonClosureJet1[i];
			tauNonClosureJet2[i]=1.0+tauNonClosureJet2[i];
			tauBMistagUp[i]=1.0+tauBMistagUp[i];
			tauBMistagDown[i]=1.0+tauBMistagDown[i];
			if(tauNonClosureWJMHT2[i]<-99):tauNonClosureWJMHT2[i]=1.0;
			else: tauNonClosureWJMHT2[i]=1.0+tauNonClosureWJMHT2[i]
			if(tauNonClosureTTbarMHT2[i]<-99):tauNonClosureTTbarMHT2[i]=1.0;
			else: tauNonClosureTTbarMHT2[i]=1.0+tauNonClosureTTbarMHT2[i]
			if(tauNonClosureWJMHT3[i]<-99):tauNonClosureWJMHT3[i]=1.0;
			else: tauNonClosureWJMHT3[i]=1.0+tauNonClosureWJMHT3[i]
			if(tauNonClosureTTbarMHT3[i]<-99):tauNonClosureTTbarMHT3[i]=1.0;
			else: tauNonClosureTTbarMHT3[i]=1.0+tauNonClosureTTbarMHT3[i]
			signalRegion.addSingleSystematic('HadTauCorrUnc'+str(i),'lnN',['WTopHad'], 1.0+tauUncCorr[i], '', i)
		#print tauNonClosureJet1[42]
		signalRegion.addSingleSystematic('HadTauNJClosureNJets0Unc','lnN',['WTopHad'],tauNonClosureJet0,'NJets0');
		signalRegion.addSingleSystematic('HadTauNJClosureNJets1Unc','lnN',['WTopHad'],tauNonClosureJet1,'NJets1');
		signalRegion.addSingleSystematic('HadTauNJClosureNJets2Unc','lnN',['WTopHad'],tauNonClosureJet2,'NJets2');
		signalRegion.addAsymSystematic('HadTauBTagShape','lnN',['WTopHad'],tauBMistagUp,tauBMistagDown,'BTags0');
		signalRegion.addAsymSystematic('HadTauBTagShape','lnN',['WTopHad'],tauBMistagUp,tauBMistagDown,'BTags1');
		signalRegion.addAsymSystematic('HadTauBTagShape','lnN',['WTopHad'],tauBMistagUp,tauBMistagDown,'BTags2');
		signalRegion.addAsymSystematic('HadTauBTagShape','lnN',['WTopHad'],tauBMistagUp,tauBMistagDown,'BTags3');
		signalRegion.addSingleSystematic("HadTauMHT1WJUnc ", 'lnN', ['WTopHad'], tauNonClosureWJMHT2, 'MHT1')
		signalRegion.addSingleSystematic("HadTauMHT1TTbarUnc ", 'lnN', ['WTopHad'], tauNonClosureTTbarMHT2, 'MHT1')	
		signalRegion.addSingleSystematic("HadTauMHT2WJUnc ", 'lnN', ['WTopHad'], tauNonClosureWJMHT3, 'MHT2')
		signalRegion.addSingleSystematic("HadTauMHT2TTbarUnc ", 'lnN', ['WTopHad'], tauNonClosureTTbarMHT3, 'MHT2')
	
	### QCD uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.qcdOnly:	

		#ListOfQCDSys = getSystematicsListQCD("inputsFromOwen/lowdphiinputs-72bins-%sifb.txt"%(str(int(3))));

		ListOfQCDSysK1 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),7)
		ListOfQCDSysK2 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),8)
		ListOfQCDSysK3 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),9)
		ListOfQCDSysK4 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),10)
		ListOfQCDSysK5 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),11)
		ListOfQCDSysK6 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),12)
		ListOfQCDSysK7 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),13)
		ListOfQCDSysK8 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),14)	
		ListOfQCDSysK9 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),15)
		ListOfQCDSysK10 = textToListStr("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),16)
		ContaminUncForLowdphiRegion = textToList("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt"%(str(int(lumi))),4);
		#ListOfQCDSys = textToList("inputsFromOwen/qcd-bg-combine-input-%sipb-v0.txt" %(str(int(lumi))),18);
		for i in range(len(tagsForSignalRegion)):
			signalRegion.addSingleSystematic("ldpCR"+str(i),'lnU','qcd',10000.,'',i);
			LowdphiControlRegion.addSingleSystematic("ldpCR"+str(i),'lnU','qcd',10000.,'',i);	
			if(ContaminForLowdphiRegion[i]>0.000001):LowdphiControlRegion.addSingleSystematic("contamUnc"+str(i), 'lnN','contam',1+(ContaminUncForLowdphiRegion[i]/ContaminForLowdphiRegion[i]),'',i)
		for i in range(len(ListOfQCDSysK1)):
			if(ListOfQCDSysK1[i]!='-'):signalRegion.addSingleSystematic("KQCDHT1",'lnN','qcd',float(ListOfQCDSysK1[i]),'',i);
			if(ListOfQCDSysK2[i]!='-'):signalRegion.addSingleSystematic("KQCDHT2",'lnN','qcd',float(ListOfQCDSysK2[i]),'',i);
			if(ListOfQCDSysK3[i]!='-'):signalRegion.addSingleSystematic("KQCDHT3",'lnN','qcd',float(ListOfQCDSysK3[i]),'',i);
			if(ListOfQCDSysK4[i]!='-'):signalRegion.addSingleSystematic("KQCDMHT2",'lnN','qcd',float(ListOfQCDSysK4[i]),'',i);
			if(ListOfQCDSysK5[i]!='-'):signalRegion.addSingleSystematic("KQCDMHT3",'lnN','qcd',float(ListOfQCDSysK5[i]),'',i);
			if(ListOfQCDSysK6[i]!='-'):signalRegion.addSingleSystematic("KQCDMHT4",'lnN','qcd',float(ListOfQCDSysK6[i]),'',i);
			if(ListOfQCDSysK7[i]!='-'):signalRegion.addSingleSystematic("KQCDNJ2",'lnN','qcd',float(ListOfQCDSysK7[i]),'',i);
			if(ListOfQCDSysK8[i]!='-'):signalRegion.addSingleSystematic("KQCDNJ3",'lnN','qcd',float(ListOfQCDSysK8[i]),'',i);
			if(ListOfQCDSysK9[i]!='-'):signalRegion.addSingleSystematic("KQCDNJ4",'lnN','qcd',float(ListOfQCDSysK9[i]),'',i);
			if(ListOfQCDSysK10[i]!='-'):signalRegion.addSingleSystematic("KQCDNJ5",'lnN','qcd',float(ListOfQCDSysK10[i]),'',i);

	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
	if options.allBkgs or options.llpOnly or  (options.tauOnly and  options.llpOnly) or options.tauOnly: SLcontrolRegion.writeCards( odir );
	# if options.allBkgs or options.tauOnly: HadcontrolRegion.writeCards( odir );
	if options.allBkgs or options.zvvOnly: sphotonRegion.writeCards( odir );
	if options.allBkgs or options.qcdOnly: LowdphiControlRegion.writeCards( odir );

