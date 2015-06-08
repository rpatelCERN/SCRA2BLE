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
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_QCD") );
	signalRegion = searchRegion('signal', ['sig','qcd'], signalRegion_hists[0])
	signalRegion.fillRates( signalRegion_hists );

	lowdphiRegion_file = TFile("../Analysis/datacards/RA2bin_LDPfixed.root");
	lowdphiRegion_hists = [];
	lowdphiRegion_hists.append( lowdphiRegion_file.Get("RA2bin_"+sms) );
	lowdphiRegion_hists.append( lowdphiRegion_file.Get("RA2bin_QCD") );
	lowdphiRegion = searchRegion('lowdphi', ['sig','qcd'], lowdphiRegion_hists[0])
	lowdphiRegion.fillRates( lowdphiRegion_hists );

	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);

	# connect the single photon CR to the signal region

	LDPSRCRconversion_SR = ["NJets0_BTags._MHT0_HT0","NJets0_BTags._MHT0_HT1","NJets0_BTags._MHT0_HT2","NJets0_BTags._MHT1_HT3","NJets0_BTags._MHT1_HT4","NJets0_BTags._MHT2_HT5",
							 "NJets1_BTags._MHT0_HT0","NJets1_BTags._MHT0_HT1","NJets1_BTags._MHT0_HT2","NJets1_BTags._MHT1_HT3","NJets1_BTags._MHT1_HT4","NJets1_BTags._MHT2_HT5",
							 "NJets2_BTags._MHT0_HT0","NJets2_BTags._MHT0_HT1","NJets2_BTags._MHT0_HT2","NJets2_BTags._MHT1_HT3","NJets2_BTags._MHT1_HT4","NJets2_BTags._MHT2_HT5"];
	LDPSRCRconversion_CR = [['HT1','MHT1','MHT2','NJets1','NJets2','NJets3'],
							 ['HT2','MHT1','MHT2','NJets1','NJets2','NJets3'], 
							 ['HT3','MHT1','MHT2','NJets1','NJets2','NJets3'], 
							 ['HT1','HT2' ,'MHT3','NJets1','NJets2','NJets3'], 
							 ['HT3','MHT3','NJets1','NJets2','NJets3'], 
							 ['HT2', 'HT3','MHT4','NJets1','NJets2','NJets3'], 
							 ['HT1','MHT1','MHT2','NJets4'],
							 ['HT2','MHT1','MHT2','NJets4'],
							 ['HT3','MHT1','MHT2','NJets4'],
							 ['HT1','HT2' ,'MHT3','NJets4'],
							 ['HT3','MHT3','NJets4'],
							 ['HT2', 'HT3','MHT4','NJets4'],
							 ['HT1','MHT1','MHT2','NJets5'],
							 ['HT2','MHT1','MHT2','NJets5'],
							 ['HT3','MHT1','MHT2','NJets5'],
							 ['HT1','HT2' ,'MHT3','NJets5'],
							 ['HT3','MHT3','NJets5'],
							 ['HT2', 'HT3','MHT4','NJets5']];
	LDPCRs    = ['HT1','HT2','HT3','MHT1','MHT2','MHT3','MHT4','NJets1','NJets2','NJets3','NJets4','NJets5'];
	LDPCRUncs = [ 1.02, 1.01, 1.03,   1.0,   1.1,   1.7,   2.5,     1.0,    1.05,    1.06,     1.1,     1.4];

	RzgammaUnc = [1.006,1.011,1.025,1.014,1.048,1.031,
				  1.043,1.048,1.09,1.1,1.171,1.179,
				  1.4,1.2,1.3,1.42,1.6,1.9 ];

	for i in range(len(LDPSRCRconversion_SR)):
		for j in range(len(LDPSRCRconversion_CR[i])):
			signalRegion.addSingleSystematic('LDPCR'+str(LDPSRCRconversion_CR[i][j]),'lnU',['qcd'],100,LDPSRCRconversion_SR[i]);
			tmpUnc = LDPCRUncs[ LDPCRs.index( LDPSRCRconversion_CR[i][j] ) ];
			signalRegion.addSingleSystematic('LDPCRUnc'+str(LDPSRCRconversion_CR[i][j]),'lnN',['qcd'],tmpUnc,LDPSRCRconversion_SR[i]);

	for i in range(len(LDPCRs)):
		lowdphiRegion.addSingleSystematic('LDPCR'+str(LDPCRs[i]),'lnU',['qcd'],100,LDPCRs[i]);

	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
	lowdphiRegion.writeCards( odir );	
