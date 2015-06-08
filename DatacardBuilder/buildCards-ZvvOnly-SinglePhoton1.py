from ROOT import *

import os
import math
import sys
from searchRegion import *
from singleBin import *

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
	signalRegion_hists = [];
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_"+sms) );
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_Zinv") );
	signalRegion = searchRegion('signal', ['sig','zvv'], signalRegion_hists[0])
	signalRegion.fillRates( signalRegion_hists );

	sphotonRegion_file = TFile("../Analysis/datacards/RA2bin_GJet_CleanVars.root");
	sphotonRegion_hists = [];
	sphotonRegion_hists.append( sphotonRegion_file.Get("RA2bin_"+sms) );
	sphotonRegion_hists.append( sphotonRegion_file.Get("RA2bin_GJet") );
	sphotonRegion = searchRegion('sphoton', ['sig','zvv'], sphotonRegion_hists[0])
	sphotonRegion.fillRates( sphotonRegion_hists );

	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);

	# connect the single photon CR to the signal region
	singlePhotonBins = ["NJets0_BTags._MHT0_HT0","NJets0_BTags._MHT0_HT1","NJets0_BTags._MHT0_HT2","NJets0_BTags._MHT1_HT3","NJets0_BTags._MHT1_HT4","NJets0_BTags._MHT2_HT5",
						"NJets1_BTags._MHT0_HT0","NJets1_BTags._MHT0_HT1","NJets1_BTags._MHT0_HT2","NJets1_BTags._MHT1_HT3","NJets1_BTags._MHT1_HT4","NJets1_BTags._MHT2_HT5",
						"NJets2_BTags._MHT0_HT0","NJets2_BTags._MHT0_HT1","NJets2_BTags._MHT0_HT2","NJets2_BTags._MHT1_HT3","NJets2_BTags._MHT1_HT4","NJets2_BTags._MHT2_HT5"];
	RzgammaUnc = [1.006,1.011,1.025,1.014,1.048,1.031,
				  1.043,1.048,1.09,1.1,1.171,1.179,
				  1.4,1.2,1.3,1.42,1.6,1.9 ];

	for i in range(len(singlePhotonBins)):
		signalRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);
		sphotonRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);
		signalRegion.addSingleSystematic('SPhoRZgUnc'+str(i),'lnN',['zvv'],RzgammaUnc[i],singlePhotonBins[i]);

	signalRegion.addSingleSystematic('SPho0BUnc','lnN',['zvv'],1.2,'BTags0');
	signalRegion.addSingleSystematic('SPho1BUnc','lnN',['zvv'],1.5,'BTags1');
	signalRegion.addSingleSystematic('SPho2BUnc','lnN',['zvv'],2.0,'BTags2');
	signalRegion.addSingleSystematic('SPho3BUnc','lnN',['zvv'],3.0,'BTags3');

	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
	sphotonRegion.writeCards( odir );	
