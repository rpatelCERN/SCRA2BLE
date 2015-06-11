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
	## 1. Fill Rates for each analysis region

	# Zmumu control region
	zmumuRegion_file = TFile("../Analysis/datacards/RA2bin_DYm_CleanVars.root");
	zmumuRegion_hists = [];
	zmumuRegion_hists.append( zmumuRegion_file.Get("RA2bin_"+sms) );
	zmumuRegion_hists.append( zmumuRegion_file.Get("RA2bin_DY") );
	zmumuRegion = searchRegion('DYmu', ['sig','zvv'], binLabelsToList(zmumuRegion_hists[0]) )
	zmumuRegion.fillRates( zmumuRegion_hists );

	# Zelel control region
	zelelRegion_file = TFile("../Analysis/datacards/RA2bin_DYe_CleanVars.root");
	zelelRegion_hists = [];
	zelelRegion_hists.append( zelelRegion_file.Get("RA2bin_"+sms) );
	zelelRegion_hists.append( zelelRegion_file.Get("RA2bin_DY") );
	zelelRegion = searchRegion('DYel', ['sig','zvv'], binLabelsToList(zelelRegion_hists[0]) )
	zelelRegion.fillRates( zelelRegion_hists );

	# signal region
	signalRegion_file = TFile("../Analysis/datacards/RA2bin_signal.root");
	signalRegion_hists = [];

	h_newZinvSRYields = hutil_clone0BtoNB(signalRegion_file.Get("RA2bin_Zinv"))
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_"+sms) );
	#signalRegion_hists.append( signalRegion_file.Get("RA2bin_Zinv") );
	signalRegion_hists.append( h_newZinvSRYields );
	
	signalRegion = searchRegion('signal', ['sig','zvv'], binLabelsToList(signalRegion_hists[0]) )
	signalRegion.fillRates( signalRegion_hists );

	zmumuRegion.writeRates();
	zelelRegion.writeRates();
	signalRegion.writeRates();

	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);

	# connect the single photon CR to the signal region
	drellyanBins = ["NJets0_BTags._MHT0_HT0","NJets0_BTags._MHT0_HT1","NJets0_BTags._MHT0_HT2","NJets0_BTags._MHT1_HT3","NJets0_BTags._MHT1_HT4","NJets0_BTags._MHT2_HT5",
						"NJets1_BTags._MHT0_HT0","NJets1_BTags._MHT0_HT1","NJets1_BTags._MHT0_HT2","NJets1_BTags._MHT1_HT3","NJets1_BTags._MHT1_HT4","NJets1_BTags._MHT2_HT5",
						"NJets2_BTags._MHT0_HT0","NJets2_BTags._MHT0_HT1","NJets2_BTags._MHT0_HT2","NJets2_BTags._MHT1_HT3","NJets2_BTags._MHT1_HT4","NJets2_BTags._MHT2_HT5"];

	DYmuStatUnc = [1.006,1.009,1.02,1.013 ,1.041 ,1.027 ,1.045 ,1.034 ,1.061 ,1.073 ,1.116 ,1.142 ,1.217 ,1.122 ,1.154 ,1.372 ,1.452 ,1.611];
	DYelStatUnc = [1.006 ,1.01 ,1.023 ,1.012 ,1.043 ,1.027 ,1.045 ,1.038 ,1.071 ,1.086 ,1.122 ,1.161 ,1.272 ,1.143 ,1.194 ,1.48 ,1.405 ,1.48];

	for i in range(len(drellyanBins)):
		signalRegion.addSingleSystematic('DYCR'+str(i),'lnU',['zvv'],100,drellyanBins[i]);
		zmumuRegion.addSingleSystematic('DYCR'+str(i),'lnU',['zvv'],100,drellyanBins[i]);
		zelelRegion.addSingleSystematic('DYCR'+str(i),'lnU',['zvv'],100,drellyanBins[i]);
		
		zmumuRegion.addSingleSystematic('DYmuStatUnc'+str(i),'lnN',['zvv'],DYmuStatUnc[i],drellyanBins[i]);		
		zelelRegion.addSingleSystematic('DYelStatUnc'+str(i),'lnN',['zvv'],DYelStatUnc[i],drellyanBins[i]);

	drellyanNBExtrap = ["NJets0_BTags1","NJets0_BTags2","NJets0_BTags3",
						"NJets1_BTags1","NJets1_BTags2","NJets1_BTags3",
						"NJets2_BTags1","NJets2_BTags2","NJets2_BTags3"];
	DYNBStatUnc = [1.074,1.148,1.492,1.079,1.159,1.502,1.12,1.195,1.561];
	for i in range(len(drellyanNBExtrap)):
		signalRegion.addSingleSystematic('DYNBStatUnc'+str(i),'lnN',['zvv'],DYNBStatUnc[i],drellyanNBExtrap[i]);

	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
	zmumuRegion.writeCards( odir );	
	zelelRegion.writeCards( odir );	




