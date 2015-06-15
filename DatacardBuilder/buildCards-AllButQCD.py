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

(options, args) = parser.parse_args()


#########################################################################################################
#########################################################################################################
if __name__ == '__main__':

	sms = options.signal;
	tag = options.tag;
	lumi = float(options.lumi);
	signalmu = float(options.mu);
	odir = 'testCards-%s-%s-%s-mu%0.1f/' % ( tag,sms,str(round(lumi,1)), signalmu );
	idir = '../Analysis/datacards_%sfb' % ( str(int(lumi)) );
	if os.path.exists(odir): os.system( "rm -r %s" % (odir) );
	os.makedirs(odir);

	print odir, signalmu

	#------------------------------------------------------------------------------------------------
	## 1. Fill Rates for each signal region

	# histogram gymnastics...
	signalRegion_file = TFile(idir+"/RA2bin_signal.root");
	sphotonRegion_file = TFile(idir+"/RA2bin_GJet_CleanVars.root");
	
	# zinv --------
	zinv_sr = signalRegion_file.Get("RA2bin_Zinv");
	gjet_cr = sphotonRegion_file.Get("RA2bin_GJet");
	h_newZinvSRYields = hutil_clone0BtoNB( zinv_sr );
	signalRegion_zvvList = binsToList( h_newZinvSRYields );

	# ll --------
	LL_file = TFile("inputsLostLepton/LLPrediction_%sfb.root" % (str(int(lumi)) ));
	LLPrediction_Hist=LL_file.Get("fullPred_LL");
	LLCS_Hist=LL_file.Get("fullCS_LL");
	LLWeight_Hist=LL_file.Get("fullWeight_LL");
	signalRegion_LLList = binsToList( LLPrediction_Hist );
	signalRegion_WeightList=binsToList(LLWeight_Hist);
	signalRegion_CSList=binsToList(LLCS_Hist)
	signalRegion_statUncList = binsToList( LL_file.Get("fullStatUp_LL") );
	signalRegion_sysUncList = textToList( "./inputsLostLepton/sysunc.txt", 0 );

	# had tau
	signalRegion_tauList = textToList( "inputsHadTau/HadTauMCPred%sfb.txt" % (str(int(lumi))), 0 );
	hadtauSystematics = textToList( "inputsHadTau/HadTauMCPred%sfb.txt" % (str(int(lumi))), 1 )

	# signal --------
	signalRegion_sigHist = signalRegion_file.Get("RA2bin_"+sms);
	tagsForSignalRegion = binLabelsToList(signalRegion_sigHist);
	signalRegion_sigList = binsToList( signalRegion_sigHist );

	# photon region
	phoRegion_sigHist = sphotonRegion_file.Get("RA2bin_"+sms)
	tagsForSinglePhoton = binLabelsToList(phoRegion_sigHist)
	phoRegion_sigList = binsToList(phoRegion_sigHist);
	phoRegion_phoList = binsToList(gjet_cr);
	contributionsPerBin = [];
	for i in range(len(tagsForSinglePhoton)): contributionsPerBin.append(['sig','zvv']);
	sphotonRegion = searchRegion('sphoton', contributionsPerBin, tagsForSinglePhoton)
	phoRegion_Rates = [];
	for i in range(sphotonRegion._nBins):
		tmpList = [];
		tmpList.append(phoRegion_sigList[i]);
		tmpList.append(phoRegion_phoList[i]);
		phoRegion_Rates.append( tmpList );
	sphotonRegion.fillRates( phoRegion_Rates );

	# signal region
	contributionsPerBin = [];
	for i in range(len(tagsForSignalRegion)): contributionsPerBin.append(['sig','WTopSL','WTopHad','zvv']);
	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)

	# accounting for LL Region
	tagsForSLControlRegion=[]	
	SLcontrolContributionsPerBin = [];
	addControl=[]
	for i in range(len(tagsForSignalRegion)): 
		if(signalRegion_CSList[i]<2):
			SLcontrolContributionsPerBin.append(['sig', 'WTopSL']);
			tagsForSLControlRegion.append(tagsForSignalRegion[i]);
			addControl.append(i);

	SLcontrolRegion = searchRegion('SLControl', SLcontrolContributionsPerBin, tagsForSLControlRegion)
	SLcontrolRegion_Obs = [];
	SLcontrolRegion_Rates = [];
	for i in range(len(addControl)):
		tmpList=[]
		tmpList.append(0);
		tmpList.append(1.);
		SLcontrolRegion_Obs.append(signalRegion_CSList[addControl[i]]);
		SLcontrolRegion_Rates.append(tmpList);

	SLcontrolRegion.fillRates(SLcontrolRegion_Rates);
	SLcontrolRegion.setObservedManually(SLcontrolRegion_Obs);

	# -------------------------------
	signalRegion_Rates = [];
	signalRegion_Obs = [];
	controlRegion_Rates=[];

	for i in range(signalRegion._nBins):
		signalRegion_Obs.append(signalRegion_sigList[i]*signalmu + signalRegion_LLList[i] + signalRegion_tauList[i] + signalRegion_zvvList[i]);

		# print signalRegion_sigList[i], (signalRegion_sigList[i]*signalmu)

		tmpList = [];
		tmpList.append(signalRegion_sigList[i]);

		# LL rate
		if(signalRegion_CSList[i]>=2):
			tmpList.append(signalRegion_LLList[i]);
		else:
			#CS=signalRegion_CSList[i]
			#if(CS<0.0001):CS=1
			tmpList.append(signalRegion_WeightList[i]); # the control region "rate" line is always going to be 1
			addControl.append(i);

		# Had Tau rate
		tmpList.append(signalRegion_tauList[i]);
		tmpList.append(signalRegion_zvvList[i]);
		signalRegion_Rates.append( tmpList );
	
	signalRegion.fillRates( signalRegion_Rates );
	signalRegion.setObservedManually(signalRegion_Obs)

	SLcontrolRegion.writeRates();
	sphotonRegion.writeRates();
	signalRegion.writeRates();

	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);

	RzgammaUnc = [1.006,1.011,1.025,1.014,1.048,1.031,
				  1.043,1.048,1.09,1.1,1.171,1.179,
				  1.4,1.2,1.3,1.42,1.6,1.9 ];

	# connect the single photon CR to the signal region
	singlePhotonBins = ["NJets0_BTags._MHT0_HT0","NJets0_BTags._MHT0_HT1","NJets0_BTags._MHT0_HT2","NJets0_BTags._MHT1_HT3","NJets0_BTags._MHT1_HT4","NJets0_BTags._MHT2_HT5",
						"NJets1_BTags._MHT0_HT0","NJets1_BTags._MHT0_HT1","NJets1_BTags._MHT0_HT2","NJets1_BTags._MHT1_HT3","NJets1_BTags._MHT1_HT4","NJets1_BTags._MHT2_HT5",
						"NJets2_BTags._MHT0_HT0","NJets2_BTags._MHT0_HT1","NJets2_BTags._MHT0_HT2","NJets2_BTags._MHT1_HT3","NJets2_BTags._MHT1_HT4","NJets2_BTags._MHT2_HT5"];

	for i in range(len(singlePhotonBins)):
		signalRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);
		sphotonRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);

	# for i in range(signalRegion.GetNbins()):
	for i in range(18): # only for the 0B bins
		# ratioI = i % 18;
		signalRegion.addSingleSystematic('SPhoRZgUnc'+str(i),'lnN',['zvv'],RzgammaUnc[i],'',i);

	#RZg data/MC double ratios from Jim H.
	signalRegion.addSingleSystematic('RZgDataUncMHT0','lnN',['zvv'],1.04,'MHT0');	
	signalRegion.addSingleSystematic('RZgDataUncMHT1','lnN',['zvv'],1.11,'MHT1');	
	signalRegion.addSingleSystematic('RZgDataUncMHT2','lnN',['zvv'],1.28,'MHT2');	
	signalRegion.addSingleSystematic('RZgDataUncNJets0','lnN',['zvv'],1.06,'NJets0');	
	signalRegion.addSingleSystematic('RZgDataUncNJets1','lnN',['zvv'],1.13,'NJets1');	
	signalRegion.addSingleSystematic('RZgDataUncNJets2','lnN',['zvv'],1.16,'NJets2');	

	# added to all bins (photon efficiency)
	signalRegion.addSingleSystematic('PhoEffUnc','lnN',['zvv'],1.2,'NJets');	
		
	# Extrpolation uncertainties, from Kevin S.
	signalRegion.addSingleSystematic('DYNBStatUncBTags1','lnN',['zvv'],1.076,'BTags1');		
	signalRegion.addSingleSystematic('DYNBStatUncBTags2','lnN',['zvv'],1.158,'BTags2');		
	signalRegion.addSingleSystematic('DYNBStatUncBTags3','lnN',['zvv'],1.507,'BTags3');		

	signalRegion.addSingleSystematic('DYNBStatUncNJets1','lnN',['zvv'],1.008,'NJets1_BTags.');		
	signalRegion.addSingleSystematic('DYNBStatUncNJets2','lnN',['zvv'],1.049,'NJets2_BTags.');		

	for i in range(signalRegion.GetNbins()):
		denom = signalRegion_LLList[i]
		if(signalRegion_CSList[i]<2):
			signalRegion.addSingleSystematic('LLSCSR'+tagsForSignalRegion[i],'lnU',['WTopSL'],100,'',i);
		else: 
			signalRegion.addSingleSystematic('LLStat'+tagsForSignalRegion[i],'lnN',['WTopSL'],1+(signalRegion_statUncList[i]/denom),'',i);					
		if(signalRegion_LLList[i]<0.00001): denom = 1.0
		signalRegion.addSingleSystematic('LLSys'+tagsForSignalRegion[i],'lnN',['WTopSL'],1+(signalRegion_sysUncList[i] / denom),'',i);
	
	for i in range(SLcontrolRegion.GetNbins()):
		SLcontrolRegion.addSingleSystematic('LLSCSR'+tagsForSLControlRegion[i],'lnU',['WTopSL'],100,'',i);		

	for i in range(signalRegion.GetNbins()):
		njetTag = tagsForSignalRegion[i].split('_')[0];
		# print njetTag
		signalRegion.addSingleSystematic('HadTauUnc'+str(i),'lnN',['WTopHadTau'],float(hadtauSystematics[i]),'',i);
	
	signalRegion.addSingleSystematic('HadTauNJClosureNJets0Unc','lnN',['WTopHadTau'],1.2,'NJets0');
	signalRegion.addSingleSystematic('HadTauNJClosureNJets1Unc','lnN',['WTopHadTau'],1.4,'NJets1');
	signalRegion.addSingleSystematic('HadTauNJClosureNJets2Unc','lnN',['WTopHadTau'],1.6,'NJets2');


	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	SLcontrolRegion.writeCards( odir );
	signalRegion.writeCards( odir );
	sphotonRegion.writeCards( odir );	
