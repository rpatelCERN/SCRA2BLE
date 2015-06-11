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
	sphotonRegion_file = TFile("../Analysis/datacards/RA2bin_GJet_CleanVars.root");

	zinv_sr = signalRegion_file.Get("RA2bin_Zinv");
	gjet_cr = sphotonRegion_file.Get("RA2bin_GJet");
	zinv_sr_normalized = zinv_sr.Clone();
	zinv_sr_normalized.Divide(gjet_cr);
	zinv_sr_normAndTrans = hutil_clone0BtoNB(zinv_sr_normalized,False); # this guy gives you the ratios in all 72 bins
	# now go back and figure out the control and signal region yields
	observedEventsInControlRegion = binsToList(gjet_cr)
	newYields = hutil_PhotonRatioFix( gjet_cr, zinv_sr_normAndTrans );
	newYieldsGJet = newYields[0];
	newYieldsZvv  = newYields[1];

	# single photon first
	sphotonRegion_hists = [];
	sphotonRegion_hists.append( sphotonRegion_file.Get("RA2bin_"+sms) );
	sphotonRegion_hists.append( newYieldsGJet );
	sphotonRegion = searchRegion('sphoton', ['sig','zvv'], sphotonRegion_hists[0])
	#normalize = True;
	sphotonRegion.fillRates( sphotonRegion_hists );
	sphotonRegion.setObservedManually( observedEventsInControlRegion );

	sphotonSingleBins = sphotonRegion._singleBins;
	observedEventsInSignalRegion = [];
	for i in range(len(sphotonSingleBins)):
		curval = sphotonSingleBins[i]._observed*binsToList(zinv_sr_normAndTrans)[i]+binsToList(signalRegion_file.Get("RA2bin_"+sms))[i];
		observedEventsInSignalRegion.append(curval);

	signalRegion_hists = [];
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_"+sms) );
	signalRegion_hists.append( newYieldsZvv );
	signalRegion = searchRegion('signal', ['sig','zvv'], signalRegion_hists[0])
	signalRegion.fillRates( signalRegion_hists );
	signalRegion.setObservedManually( observedEventsInSignalRegion );

	sphotonRegion.writeRates();
	signalRegion.writeRates();

	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);

	RzgammaUnc = [1.006,1.011,1.025,1.014,1.048,1.031,
				  1.043,1.048,1.09,1.1,1.171,1.179,
				  1.4,1.2,1.3,1.42,1.6,1.9 ];

	for i in range(signalRegion.GetNbins()):
		signalRegion.addSingleSystematic('PhotonCR'+str(i),'lnU',['zvv'],100,'',i);
		sphotonRegion.addSingleSystematic('PhotonCR'+str(i),'lnU',['zvv'],100,'',i);
		ratioI = i % 18;
		signalRegion.addSingleSystematic('SPhoRZgUnc'+str(ratioI),'lnN',['zvv'],RzgammaUnc[ratioI],'',i);


	# # connect the single photon CR to the signal region
	# singlePhotonBins = ["NJets0_BTags._MHT0_HT0","NJets0_BTags._MHT0_HT1","NJets0_BTags._MHT0_HT2","NJets0_BTags._MHT1_HT3","NJets0_BTags._MHT1_HT4","NJets0_BTags._MHT2_HT5",
	# 					"NJets1_BTags._MHT0_HT0","NJets1_BTags._MHT0_HT1","NJets1_BTags._MHT0_HT2","NJets1_BTags._MHT1_HT3","NJets1_BTags._MHT1_HT4","NJets1_BTags._MHT2_HT5",
	# 					"NJets2_BTags._MHT0_HT0","NJets2_BTags._MHT0_HT1","NJets2_BTags._MHT0_HT2","NJets2_BTags._MHT1_HT3","NJets2_BTags._MHT1_HT4","NJets2_BTags._MHT2_HT5"];

	# for i in range(len(singlePhotonBins)):
	# 	signalRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);
	# 	sphotonRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);
	# 	signalRegion.addSingleSystematic('SPhoRZgUnc'+str(i),'lnN',['zvv'],RzgammaUnc[i],singlePhotonBins[i]);

	signalRegion.addSingleSystematic('SPho0BUnc','lnN',['zvv'],1.2,'BTags0');
	signalRegion.addSingleSystematic('SPho1BUnc','lnN',['zvv'],1.5,'BTags1');
	signalRegion.addSingleSystematic('SPho2BUnc','lnN',['zvv'],2.0,'BTags2');
	signalRegion.addSingleSystematic('SPho3BUnc','lnN',['zvv'],3.0,'BTags3');

	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
	sphotonRegion.writeCards( odir );	
