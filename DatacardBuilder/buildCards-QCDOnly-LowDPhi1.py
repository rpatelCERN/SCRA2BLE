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
	signalRegion_file = TFile("../Analysis/datacards/RA2bin_signal.root");
	lowdphiRegion_file = TFile("../Analysis/datacards/RA2bin_LDP.root");

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
		if lowdphiRegion_qcdList[i] < 1: 
			tmpList.append(1.);
			QCDCRDict_TagToRate[qcdcurtag] = 1.
		else: 
			tmpList.append(lowdphiRegion_qcdList[i]);
			QCDCRDict_TagToRate[qcdcurtag] = lowdphiRegion_qcdList[i]
		#print qcdcurtag
		QCDCRDict_TagToObs[qcdcurtag] = lowdphiRegion_qcdList[i]
		lowdphiRegion_Rates.append( tmpList );

	lowdphiRegion.fillRates( lowdphiRegion_Rates );
	lowdphiRegion.setObservedManually( lowdphiRegion_qcdList )
	lowdphiRegion.writeRates();

	# signal region stuff
	signalRegion_sigHist = signalRegion_file.Get("RA2bin_"+sms);
	tagsForSignalRegion = binLabelsToList(signalRegion_sigHist)
	
	#qcd gymnastics for owen
	contributionsPerBinForSignal = [];
	ratiosPerContributionForSignal = [];
	ratesPerContributionForSignal = [];
	HTDict  = { 'HT0':['HT0'], 'HT1':['HT1'], 'HT2':['HT2'], 'HT3':['HT0','HT1'], 'HT4':['HT2'], 'HT5':['HT1','HT2'] };
	MHTDict = { 'MHT0':['MHT0','MHT1'], 'MHT1':['MHT2'], 'MHT2':['MHT3'] };
	NJDict  = { 'NJets0':['NJets0','NJets1','NJets2'], 'NJets1':['NJets3'], 'NJets2':['NJets4'] };
	kappaHTDict  =  { 'HT0':0.062,'HT1':0.048,'HT2':0.036 }
	kappaMHTDict =  { 'MHT0':1.0,'MHT1':0.472,'MHT2':0.328,'MHT3':0.308 }
	kappaNJDict  =  { 'NJets0':1.0,'NJets1':1.45,'NJets2':1.45,'NJets3':2.11,'NJets4':4.0 }
	for i in range(len(tagsForSignalRegion)):
		curtag = tagsForSignalRegion[i];
		curtaglist = curtag.split('_');
		translatedBins = [];
		translatedBins.append('sig');
		kappaRatios = [];
		ratesFromKappas = [];
		for val0 in NJDict[curtaglist[0]]:
			for val1 in MHTDict[curtaglist[2]]:
				for val2 in HTDict[curtaglist[3]]:
					qcdkey = 'qcd'+val0+curtaglist[1]+val1+val2;
					curratio = kappaNJDict[val0]*kappaMHTDict[val1]*kappaHTDict[val2];
					#print qcdkey
					
					cursignalyield = curratio*QCDCRDict_TagToRate[qcdkey];
					#print QCDCRDict_TagToRate[qcdkey]
					translatedBins.append(qcdkey);
					kappaRatios.append( curratio )
					ratesFromKappas.append( cursignalyield );
		contributionsPerBinForSignal.append( translatedBins );
		ratiosPerContributionForSignal.append( kappaRatios );
		ratesPerContributionForSignal.append( ratesFromKappas );

	signalRegion = searchRegion('signal', contributionsPerBinForSignal, tagsForSignalRegion);
	signalRegion_sigList = binsToList( signalRegion_sigHist );
	signalRegion_Rates = [];
	signalRegion_Observed = [];
	for i in range(signalRegion._nBins):
		curobs = 0;
		currate = [];
		currate.append( signalRegion_sigList[i] )
		curobs += signalRegion_sigList[i];
		for j in range(len( ratiosPerContributionForSignal[i] )):
			currate.append( ratesPerContributionForSignal[i][j] );
			# print ratiosPerContributionForSignal[i][j],QCDCRDict_TagToObs[contributionsPerBinForSignal[i][j+1]]
			curobs += ratiosPerContributionForSignal[i][j]*QCDCRDict_TagToObs[contributionsPerBinForSignal[i][j+1]]
		signalRegion_Rates.append( currate );
		signalRegion_Observed.append( curobs );

	signalRegion.fillRates( signalRegion_Rates );
	signalRegion.setObservedManually( signalRegion_Observed );
	signalRegion.writeRates();

		# listOfQCDProcesses = [];
		# for trans1 in HTtranslation:
		# 	for trans2 in MHTtranslation:
		# 		for trans3 in NJtranslation:
		# 			for trans4 in NBtranslation:
		# 				if trans1[0] in curtag and trans2[0] in curtag and trans3[0] in curtag and trans4[0] in curtag: 

	# print contributionsPerBin

	# lowdphiRegion_sigHist = lowdphiRegion_file.Get("RA2bin_"+sms);



	# signalRegion_file = TFile("../Analysis/datacards/RA2bin_signal.root");
	# signalRegion_hists = [];
	# signalRegion_hists.append( signalRegion_file.Get("RA2bin_"+sms) );
	# signalRegion_hists.append( signalRegion_file.Get("RA2bin_QCD") );
	# signalRegion = searchRegion('signal', ['sig','qcd'], signalRegion_hists[0])
	# signalRegion.fillRates( signalRegion_hists );

	# lowdphiRegion_file = TFile("../Analysis/datacards/RA2bin_LDPfixed.root");
	# lowdphiRegion_hists = [];
	# lowdphiRegion_hists.append( lowdphiRegion_file.Get("RA2bin_"+sms) );
	# lowdphiRegion_hists.append( lowdphiRegion_file.Get("RA2bin_QCD") );
	# lowdphiRegion = searchRegion('lowdphi', ['sig','qcd'], lowdphiRegion_hists[0])
	# lowdphiRegion.fillRates( lowdphiRegion_hists );

	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);
	for i in range(signalRegion._nBins):
		for j in range(1,len( contributionsPerBinForSignal[i] )):
			binname = contributionsPerBinForSignal[i][j];
			sysname = 'QCDCR'+binname;
			signalRegion.addSingleSystematic(sysname,'lnU',[binname],100,'',i);
	
        kappaUncHTDict  =  { 'HT0':1.089,'HT1':1.080,'HT2':1.0465 }
        kappaUncMHTDict =  { 'MHT0':1.0001,'MHT1':1.070,'MHT2':1.116,'MHT3':1.198 }
        kappaUncNJDict  =  { 'NJets0':1.0001,'NJets1':1.0771,'NJets2':1.124,'NJets3':1.156,'NJets4':1.397}	
#	for i in range(signalRegion._nBins):
#                for j in range(1,len( contributionsPerBinForSignal[i] )):
#			binname = contributionsPerBinForSignal[i][j];
#			print binname
	for i in range(lowdphiRegion._nBins):
		curtag = tagsForLowDPhiRegion[i];
		curtagS=curtag.split('_');
		qcdcurtag = 'qcd'+curtag.replace('_','');
		sysname = 'QCDCR'+qcdcurtag;
		kappaUncNJDict[curtagS[0]]
		kappaUncMHTDict[curtagS[2]]
	        kappaUncHTDict[curtagS[3]]	
		#print qcdcurtag
		sysname1 = 'KappaUnc'+curtagS[0]	
		sysname2 = 'KappaUnc'+curtagS[2]
                sysname3 = 'KappaUnc'+curtagS[3]
		lowdphiRegion.addSingleSystematic(sysname1,'lnN',[qcdcurtag],kappaUncNJDict[curtagS[0]],'',i);
                lowdphiRegion.addSingleSystematic(sysname2,'lnN',[qcdcurtag],kappaUncMHTDict[curtagS[2]],'',i);
                lowdphiRegion.addSingleSystematic(sysname3,'lnN',[qcdcurtag],kappaUncHTDict[curtagS[3]],'',i);
		lowdphiRegion.addSingleSystematic(sysname,'lnU',[qcdcurtag],100,'',i);


	# # connect the single photon CR to the signal region

	# LDPSRCRconversion_SR = ["NJets0_BTags._MHT0_HT0","NJets0_BTags._MHT0_HT1","NJets0_BTags._MHT0_HT2","NJets0_BTags._MHT1_HT3","NJets0_BTags._MHT1_HT4","NJets0_BTags._MHT2_HT5",
	# 						 "NJets1_BTags._MHT0_HT0","NJets1_BTags._MHT0_HT1","NJets1_BTags._MHT0_HT2","NJets1_BTags._MHT1_HT3","NJets1_BTags._MHT1_HT4","NJets1_BTags._MHT2_HT5",
	# 						 "NJets2_BTags._MHT0_HT0","NJets2_BTags._MHT0_HT1","NJets2_BTags._MHT0_HT2","NJets2_BTags._MHT1_HT3","NJets2_BTags._MHT1_HT4","NJets2_BTags._MHT2_HT5"];
	# LDPSRCRconversion_CR = [['HT1','MHT1','MHT2','NJets1','NJets2','NJets3'],
	# 						 ['HT2','MHT1','MHT2','NJets1','NJets2','NJets3'], 
	# 						 ['HT3','MHT1','MHT2','NJets1','NJets2','NJets3'], 
	# 						 ['HT1','HT2' ,'MHT3','NJets1','NJets2','NJets3'], 
	# 						 ['HT3','MHT3','NJets1','NJets2','NJets3'], 
	# 						 ['HT2', 'HT3','MHT4','NJets1','NJets2','NJets3'], 
	# 						 ['HT1','MHT1','MHT2','NJets4'],
	# 						 ['HT2','MHT1','MHT2','NJets4'],
	# 						 ['HT3','MHT1','MHT2','NJets4'],
	# 						 ['HT1','HT2' ,'MHT3','NJets4'],
	# 						 ['HT3','MHT3','NJets4'],
	# 						 ['HT2', 'HT3','MHT4','NJets4'],
	# 						 ['HT1','MHT1','MHT2','NJets5'],
	# 						 ['HT2','MHT1','MHT2','NJets5'],
	# 						 ['HT3','MHT1','MHT2','NJets5'],
	# 						 ['HT1','HT2' ,'MHT3','NJets5'],
	# 						 ['HT3','MHT3','NJets5'],
	# 						 ['HT2', 'HT3','MHT4','NJets5']];
	# LDPCRs    = ['HT1','HT2','HT3','MHT1','MHT2','MHT3','MHT4','NJets1','NJets2','NJets3','NJets4','NJets5'];
	# LDPCRUncs = [ 1.02, 1.01, 1.03,   1.0,   1.1,   1.7,   2.5,     1.0,    1.05,    1.06,     1.1,     1.4];

	# RzgammaUnc = [1.006,1.011,1.025,1.014,1.048,1.031,
	# 			  1.043,1.048,1.09,1.1,1.171,1.179,
	# 			  1.4,1.2,1.3,1.42,1.6,1.9 ];

	# for i in range(len(LDPSRCRconversion_SR)):
	# 	for j in range(len(LDPSRCRconversion_CR[i])):
	# 		signalRegion.addSingleSystematic('LDPCR'+str(LDPSRCRconversion_CR[i][j]),'lnU',['qcd'],100,LDPSRCRconversion_SR[i]);
	# 		tmpUnc = LDPCRUncs[ LDPCRs.index( LDPSRCRconversion_CR[i][j] ) ];
	# 		signalRegion.addSingleSystematic('LDPCRUnc'+str(LDPSRCRconversion_CR[i][j]),'lnN',['qcd'],tmpUnc,LDPSRCRconversion_SR[i]);

	# for i in range(len(LDPCRs)):
	# 	lowdphiRegion.addSingleSystematic('LDPCR'+str(LDPCRs[i]),'lnU',['qcd'],100,LDPCRs[i]);

	# # #------------------------------------------------------------------------------------------------
	# # ## 3. Write Cards
	signalRegion.writeCards( odir );
	lowdphiRegion.writeCards( odir );	
