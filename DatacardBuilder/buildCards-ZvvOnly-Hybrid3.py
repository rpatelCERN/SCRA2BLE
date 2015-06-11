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

	# single photon first
	sphotonRegion_hists = [];
	sphotonRegion_hists.append( sphotonRegion_file.Get("RA2bin_"+sms) );
	sphotonRegion_hists.append( gjet_cr );
	tagsForSinglePhoton = binLabelsToList(sphotonRegion_hists[0])
	sphotonRegion = searchRegion('sphoton', ['sig','zvv'], tagsForSinglePhoton)
	#normalize = True;
	sphotonRegion.fillRates( sphotonRegion_hists );

	signalRegion_hists = [];
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_"+sms) );
	signalRegion_hists.append( h_newZinvSRYields );
	tagsForSignalRegion = binLabelsToList(signalRegion_hists[0]);	
	signalRegion = searchRegion('signal', ['sig','zvv'], tagsForSignalRegion)
	signalRegion.fillRates( signalRegion_hists );
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

	for i in range(signalRegion.GetNbins()):
		ratioI = i % 18;
		signalRegion.addSingleSystematic('SPhoRZgUnc'+str(ratioI),'lnN',['zvv'],RzgammaUnc[ratioI],'',i);
		
	drellyanNBExtrap = ["NJets0_BTags1","NJets0_BTags2","NJets0_BTags3",
						"NJets1_BTags1","NJets1_BTags2","NJets1_BTags3",
						"NJets2_BTags1","NJets2_BTags2","NJets2_BTags3"];
	DYNBStatUnc = [1.074,1.148,1.492,1.079,1.159,1.502,1.12,1.195,1.561];
	for i in range(len(drellyanNBExtrap)):
		signalRegion.addSingleSystematic('DYNBStatUnc'+str(i),'lnN',['zvv'],DYNBStatUnc[i],drellyanNBExtrap[i]);
		
	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
	sphotonRegion.writeCards( odir );	
