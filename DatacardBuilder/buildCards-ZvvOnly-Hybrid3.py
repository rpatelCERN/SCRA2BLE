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
	sphotonRegion_file = TFile("../Analysis/datacards/RA2bin_GJet_CleanVars-18bins.root");

	zinv_sr = signalRegion_file.Get("RA2bin_Zinv");
	gjet_cr = sphotonRegion_file.Get("RA2bin_GJet");
	h_newZinvSRYields = hutil_clone0BtoNB( zinv_sr );

	# photon region
	phoRegion_sigHist = sphotonRegion_file.Get("RA2bin_"+sms)
	tagsForSinglePhoton = binLabelsToList(phoRegion_sigHist)
	phoRegion_sigList = binsToList(phoRegion_sigHist);
	phoRegion_phoList = binsToList(gjet_cr);
	contributionsPerBin = [];
	for i in range(len(tagsForSinglePhoton)): contributionsPerBin.append(['sig','zvv']);
	sphotonRegion = searchRegion('sphoton', contributionsPerBin, tagsForSinglePhoton)
	#normalize = True;
	phoRegion_Rates = [];
	for i in range(sphotonRegion._nBins):
		tmpList = [];
		tmpList.append(phoRegion_sigList[i]);
		tmpList.append(phoRegion_phoList[i]);
		phoRegion_Rates.append( tmpList );
	sphotonRegion.fillRates( phoRegion_Rates );

	# signal region
	signalRegion_sigHist = signalRegion_file.Get("RA2bin_"+sms);
	tagsForSignalRegion = binLabelsToList(signalRegion_sigHist);
	signalRegion_sigList = binsToList( signalRegion_sigHist );
	signalRegion_zvvList = binsToList( h_newZinvSRYields );
	contributionsPerBin = [];
	for i in range(len(tagsForSignalRegion)): contributionsPerBin.append(['sig','zvv']);
	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)
	signalRegion_Rates = [];
	for i in range(signalRegion._nBins):
		tmpList = [];
		tmpList.append(signalRegion_sigList[i]);
		tmpList.append(signalRegion_zvvList[i]);
		signalRegion_Rates.append( tmpList );
	signalRegion.fillRates( signalRegion_Rates );

	# signalRegion.setObservedManually( observedEventsInSignalRegion );

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
		signalRegion.addSingleSystematic('SPhoRZgUnc'+str(ratioI),'lnN',['zvv'],RzgammaUnc[i],'',i);

	#RZg data/MC double ratios from Jim H.
	signalRegion.addSingleSystematic('RZgDataUncMHT0','lnN',['zvv'],1.04,'MHT0');	
	signalRegion.addSingleSystematic('RZgDataUncMHT1','lnN',['zvv'],1.11,'MHT1');	
	signalRegion.addSingleSystematic('RZgDataUncMHT2','lnN',['zvv'],1.28,'MHT2');	
	signalRegion.addSingleSystematic('RZgDataUncNJets0','lnN',['zvv'],1.06,'NJets0');	
	signalRegion.addSingleSystematic('RZgDataUncNJets1','lnN',['zvv'],1.13,'NJets1');	
	signalRegion.addSingleSystematic('RZgDataUncNJets2','lnN',['zvv'],1.16,'NJets2');	

	# added to all bins (photon efficiency)
	signalRegion.addSingleSystematic('PhoEffUnc','lnN',['zvv'],1.2,'NJets');	
		
	# drellyanNBExtrap = ["NJets0_BTags1","NJets0_BTags2","NJets0_BTags3",
	# 					"NJets1_BTags1","NJets1_BTags2","NJets1_BTags3",
	# 					"NJets2_BTags1","NJets2_BTags2","NJets2_BTags3"];
	# DYNBStatUnc = [1.074,1.148,1.492,1.079,1.159,1.502,1.12,1.195,1.561];
	# for i in range(len(drellyanNBExtrap)):
	# 	signalRegion.addSingleSystematic('DYNBStatUnc'+str(i),'lnN',['zvv'],DYNBStatUnc[i],drellyanNBExtrap[i]);
		
	# Extrpolation uncertainties, from Kevin S.
	signalRegion.addSingleSystematic('DYNBStatUncBTags1','lnN',['zvv'],1.076,'BTags1');		
	signalRegion.addSingleSystematic('DYNBStatUncBTags2','lnN',['zvv'],1.158,'BTags2');		
	signalRegion.addSingleSystematic('DYNBStatUncBTags3','lnN',['zvv'],1.507,'BTags3');		

	signalRegion.addSingleSystematic('DYNBStatUncNJets1','lnN',['zvv'],1.008,'NJets1_BTags.');		
	signalRegion.addSingleSystematic('DYNBStatUncNJets2','lnN',['zvv'],1.049,'NJets2_BTags.');		

	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
	sphotonRegion.writeCards( odir );	
