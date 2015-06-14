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
(options, args) = parser.parse_args()


#########################################################################################################
#########################################################################################################
if __name__ == '__main__':

	sms = options.signal;
	tag = options.tag;
	odir = 'testCards-%s-%s/' % (tag,sms);
	if not os.path.exists(odir): os.makedirs(odir);

	#------------------------------------------------------------------------------------------------
	## 1. Fill Rates for each signal region

	# histogram gymnastics...
	signalRegion_file = TFile("../Analysis/datacards/RA2bin_signal.root");
	LL_file = TFile("inputsLostLepton/LLPrediction_10fb.root");
	LLPrediction_Hist=LL_file.Get("fullPred_LL");
	LLCS_Hist=LL_file.Get("fullCS_LL");
	LLWeight_Hist=LL_file.Get("fullWeight_LL");
	# signal region
	signalRegion_sigHist = signalRegion_file.Get("RA2bin_"+sms);
	tagsForSignalRegion = binLabelsToList(signalRegion_sigHist);
	signalRegion_sigList = binsToList( signalRegion_sigHist );
	signalRegion_LLList = binsToList( LLPrediction_Hist );
	signalRegion_WeightList=binsToList(LLWeight_Hist);
	signalRegion_CSList=binsToList(LLCS_Hist)
	signalRegion_statUncList = textToList( "./inputsLostLepton/statunc.txt", 0 );
	signalRegion_sysUncList = textToList( "./inputsLostLepton/sysunc.txt", 0 );
	# print signalRegion_sysUncList
	tagsForControlRegion=[]
	contributionsPerBin = [];
	ControlcontributionsPerBin = [];
	for i in range(len(tagsForSignalRegion)): contributionsPerBin.append(['sig','WTopSL']);
	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)
	for i in range(len(tagsForSignalRegion)): 
		if(signalRegion_CSList[i]<2):
			ControlcontributionsPerBin.append(['sig', 'WTopSL']);
			tagsForControlRegion.append(tagsForSignalRegion[i]);

		## nhan validation
		# if signalRegion_CSList[i] >= 2: print i,signalRegion_sigList[i], signalRegion_LLList[i], signalRegion_WeightList[i], signalRegion_CSList[i], signalRegion_statUncList[i], signalRegion_sysUncList[i];
		# if signalRegion_CSList[i] < 2: print i,signalRegion_sigList[i], signalRegion_LLList[i], signalRegion_WeightList[i], signalRegion_CSList[i], signalRegion_statUncList[i], signalRegion_sysUncList[i], "hey-oh!"

	controlRegion = searchRegion('SLControl', ControlcontributionsPerBin, tagsForControlRegion)
	
	signalRegion_Rates = [];
	signalRegion_Obs = [];
	controlRegion_Rates=[];
	addControl=[]
	for i in range(signalRegion._nBins):
		signalRegion_Obs.append(signalRegion_sigList[i] + signalRegion_LLList[i]);

		tmpList = [];
		tmpList.append(signalRegion_sigList[i]);
		if(signalRegion_CSList[i]>=2):
			tmpList.append(signalRegion_LLList[i]);
		else:
			#CS=signalRegion_CSList[i]
			#if(CS<0.0001):CS=1
			tmpList.append(signalRegion_WeightList[i]); # the control region "rate" line is always going to be 1
			addControl.append(i);
		signalRegion_Rates.append( tmpList );
 	
 	controlRegion_Obs = [];
	for i in range(len(addControl)):
		tmpList=[]
		tmpList.append(0);
		tmpList.append(1.);
		controlRegion_Obs.append(signalRegion_CSList[addControl[i]]);
		controlRegion_Rates.append(tmpList);
	
	signalRegion.fillRates( signalRegion_Rates );
	signalRegion.setObservedManually( signalRegion_Obs );
	signalRegion.writeRates();

	controlRegion.fillRates(controlRegion_Rates);
	controlRegion.setObservedManually(controlRegion_Obs);
	controlRegion.writeRates();

	## -------------- systematics time! ------------------

	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);

	for i in range(signalRegion.GetNbins()):
		if(signalRegion_CSList[i]<2):
			signalRegion.addSingleSystematic('LLSCSR'+tagsForSignalRegion[i],'lnU',['WTopSL'],100,'',i);
		den=signalRegion_LLList[i]
		if(signalRegion_LLList[i]<0.00001):den=1.0
		signalRegion.addSingleSystematic('LLStat'+tagsForSignalRegion[i],'lnN',['WTopSL'],1+(signalRegion_statUncList[i]/den),'',i);					
		signalRegion.addSingleSystematic('LLSys'+tagsForSignalRegion[i],'lnN',['WTopSL'],1+(signalRegion_sysUncList[i]/den),'',i);
	
	for i in range(controlRegion.GetNbins()):
		controlRegion.addSingleSystematic('LLSCSR'+tagsForControlRegion[i],'lnU',['WTopSL'],100,'',i);		
	
	## -------------- write it out ------------------
	signalRegion.writeCards(odir);
	controlRegion.writeCards(odir);
