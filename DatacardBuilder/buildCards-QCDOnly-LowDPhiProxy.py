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
	signalRegion_file = TFile("../Analysis/datacards_3fb/RA2bin_signal.root");
	lowdphiRegion_file = TFile("../Analysis/datacards_10fb/RA2bin_LDP.root");
	# signal region stuff
	signalRegion_sigHist = signalRegion_file.Get("RA2bin_"+sms);
	tagsForSignalRegion = binLabelsToList(signalRegion_sigHist)
	
	#qcd gymnastics for owen
	contributionsPerBinForSignal = [];
	ratiosPerContributionForSignal = [];
	ratesPerContributionForSignal = [];

	# low dphi region stuff
	lowdphiRegion_sigHist = lowdphiRegion_file.Get("RA2bin_"+sms);
	tagsForLowDPhiRegion = binLabelsToList(lowdphiRegion_sigHist)
	contributionsPerBin = [];
	for i in range(len(tagsForLowDPhiRegion)): 
		curtag = tagsForLowDPhiRegion[i];
		qcdcurtag = 'qcd'+curtag.replace('_','');
		contributionsPerBin.append( [ 'sig',qcdcurtag ] );
	lowdphiRegion = searchRegion('lowdphi', contributionsPerBin, tagsForLowDPhiRegion)
	lowdphiRegion_sigList = binsToList(lowdphiRegion_sigHist);
	lowdphiRegion_qcdList = textToList('inputsFromOwen/NCR_LDP.txt',3);
	lowdphiRegion_Rates = [];
	QCDCRDict_TagToObs = {};
	QCDCRDict_TagToRate = {};
	for i in range(lowdphiRegion._nBins):
		curtag = tagsForLowDPhiRegion[i];
		qcdcurtag = 'qcd'+curtag.replace('_','');
		tmpList = [];
		###tmpList.append(lowdphiRegion_sigList[i]); ## fake this for now
		tmpList.append(0.);
#		if lowdphiRegion_qcdList[i] < 1: 
#			tmpList.append(1.);
#			QCDCRDict_TagToRate[qcdcurtag] = 1.
#		else: 
		tmpList.append(lowdphiRegion_qcdList[i]);
		QCDCRDict_TagToRate[qcdcurtag] = lowdphiRegion_qcdList[i]
		
		#print qcdcurtag
		QCDCRDict_TagToObs[qcdcurtag] = lowdphiRegion_qcdList[i]
		lowdphiRegion_Rates.append( tmpList );

#	lowdphiRegion.fillRates( lowdphiRegion_Rates );
#	lowdphiRegion.setObservedManually( lowdphiRegion_qcdList )

	HTDict  = { 'HT0':['HT0'], 'HT1':['HT1'], 'HT2':['HT2'], 'HT3':['HT0','HT1'], 'HT4':['HT2'], 'HT5':['HT1','HT2'] };
	MHTDict = { 'MHT0':['MHT0','MHT1'], 'MHT1':['MHT2'], 'MHT2':['MHT3'] };
	NJDict  = { 'NJets0':['NJets0','NJets1','NJets2'], 'NJets1':['NJets3'], 'NJets2':['NJets4'] };
	kappaHTDict  =  { 'HT0':0.062,'HT1':0.048,'HT2':0.036 }
	kappaMHTDict =  { 'MHT0':1.0,'MHT1':0.472,'MHT2':0.328,'MHT3':0.308 }
	kappaNJDict  =  { 'NJets0':1.0,'NJets1':1.45,'NJets2':1.45,'NJets3':2.11,'NJets4':4.0 }
	kappaUncHTDict  =  { 'HT0':1.089,'HT1':1.080,'HT2':1.0465 }

        kappaUncMHTDict =  { 'MHT0':0.000,'MHT1':0.080,'MHT2':0.16,'MHT3':0.30 }
        kappaUncNJDict  =  { 'NJets0':0.0000,'NJets1':0.015,'NJets2':0.15,'NJets3':0.30,'NJets4':2.0}
        kappaUncHTDict  =  { 'HT0':0.01,'HT1':0.008,'HT2':0.006 }
#        kappaUncMHTDict =  { 'MHT0':1.0001,'MHT1':1.070,'MHT2':1.116,'MHT3':1.198 }
#        kappaUncNJDict  =  { 'NJets0':1.0001,'NJets1':1.0771,'NJets2':1.124,'NJets3':1.156,'NJets4':1.397} 
	TotalLowdphiRegion_Rates = [];
	for i in range(len(tagsForSignalRegion)):
		curtag = tagsForSignalRegion[i];
		curtaglist = curtag.split('_');
		translatedBins = [];
		translatedBins.append('sig');
		kappaRatios = [];
		ratesFromKappas = [];
		tmp=0;
		tmp2=0;
		for val0 in NJDict[curtaglist[0]]:
			for val1 in MHTDict[curtaglist[2]]:
				for val2 in HTDict[curtaglist[3]]:
					qcdlookupkey='qcd'+val0+curtaglist[1]+val1+val2;
					tmp=kappaNJDict[val0]*kappaMHTDict[val1]*kappaHTDict[val2]*QCDCRDict_TagToRate[qcdlookupkey]+tmp;
					tmp2=QCDCRDict_TagToRate[qcdlookupkey]+tmp2
					#curratio = kappaNJDict[val0]*kappaMHTDict[val1]*kappaHTDict[val2];
					#print qcdkey
					#cursignalyield = curratio*QCDCRDict_TagToRate[qcdkey];
					#print QCDCRDict_TagToRate[qcdkey]
		#print " bin %d  qcd yield  %2.2f" %(i, tmp)
		translatedBins.append('qcd');
		kappaRatios.append( tmp )
		ratesFromKappas.append( tmp );
		contributionsPerBinForSignal.append( translatedBins );
		ratiosPerContributionForSignal.append( tmp );
		ratesPerContributionForSignal.append( tmp );
		TotalLowdphiRegion_Rates.append(tmp2);
	#for i in range(0, len(contributionsPerBinForSignal)):
	#	print contributionsPerBinForSignal[i]
	signalRegion = searchRegion('signal', contributionsPerBinForSignal, tagsForSignalRegion);
	signalRegion_sigList = binsToList( signalRegion_sigHist );
	#print len(signalRegion_sigList)
	NewControlRegion = searchRegion('Lowdphi', contributionsPerBinForSignal, tagsForSignalRegion);
        signalRegion_sigList = binsToList( signalRegion_sigHist );
	signalRegion_Rates = [];
	signalRegion_Observed = [];
	controlRegion_Rates = [];
        controllRegion_Observed = [];
	for i in range(signalRegion._nBins):
		curobs = 0;
		currate = [];
		curobsC = 0;
                currateC = [];
		currate.append( signalRegion_sigList[i] )
		currateC.append(0)
		curobs += signalRegion_sigList[i];
		#for j in range(len( ratiosPerContributionForSignal[i] )):
		currate.append( ratesPerContributionForSignal[i] );
		currateC.append(TotalLowdphiRegion_Rates[i]);
		# print ratiosPerContributionForSignal[i][j],QCDCRDict_TagToObs[contributionsPerBinForSignal[i][j+1]]
		#print ratesPerContributionForSignal[i], TotalLowdphiRegion_Rates[i]
		#print len(tagsForSignalRegion);
		curobs += ratesPerContributionForSignal[i];
		curobsC+= TotalLowdphiRegion_Rates[i]
		signalRegion_Rates.append( currate );
		signalRegion_Observed.append( curobs );
		controlRegion_Rates.append(currateC);
		controllRegion_Observed.append(curobsC);	
	#print len(signalRegion_Rates), len(signalRegion_Observed)
	signalRegion.fillRates( signalRegion_Rates );
	signalRegion.setObservedManually( signalRegion_Observed );
	signalRegion.writeRates();
	NewControlRegion.fillRates(controlRegion_Rates);
	NewControlRegion.setObservedManually(controllRegion_Observed);
	NewControlRegion.writeRates();

	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	logNormalUnc=[]
	for i in range(len(tagsForSignalRegion)):
        #for i in range(0,1):
                curtag = tagsForSignalRegion[i];
                curtaglist = curtag.split('_');
                translatedBins = [];
                translatedBins.append('sig');
#                kappaRatios = [];
#                uncFromKappas = [];
		sumQCDQuad=0;
		
                for val0 in NJDict[curtaglist[0]]:
                        for val1 in MHTDict[curtaglist[2]]:
                                for val2 in HTDict[curtaglist[3]]:
                                        qcdlookupkey='qcd'+val0+curtaglist[1]+val1+val2;
					qcdNJUncRatio=kappaUncNJDict[val0]/kappaNJDict[val0]
					qcdHTUncRatio=kappaUncHTDict[val2]/kappaHTDict[val2]
                                        qcdMHTUncRatio=kappaUncMHTDict[val1]/kappaMHTDict[val1]
					qcdControlYield=QCDCRDict_TagToRate[qcdlookupkey]
					sumquad=(qcdNJUncRatio*qcdNJUncRatio)+(qcdHTUncRatio*qcdHTUncRatio)+(qcdMHTUncRatio*qcdMHTUncRatio)
					sumQCDQuad+=(sqrt(sumquad)*qcdControlYield)

		den=TotalLowdphiRegion_Rates[i]
		if(den<0.000001):den=1.0
		unc=1+((sumQCDQuad)/den)
		logNormalUnc.append(unc)

	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);
	for i in range(signalRegion._nBins):
		sysLN="Logqcd%d" %i
		sysLNU="Ratioqcd%d" %i
		signalRegion.addSingleSystematic(sysLNU,'lnU','qcd',100,'',i);
		signalRegion.addSingleSystematic(sysLN,'lnN','qcd',logNormalUnc[i],'',i);
		NewControlRegion.addSingleSystematic(sysLNU,'lnU','qcd',100,'',i);
	# # connect the single photon CR to the signal region
	# # ## 3. Write Cards
	signalRegion.writeCards( odir );
	NewControlRegion.writeCards( odir );	
