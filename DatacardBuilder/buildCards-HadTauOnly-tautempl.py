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

	# signal region
	signalRegion_sigHist = signalRegion_file.Get("RA2bin_"+sms);
	tagsForSignalRegion = binLabelsToList(signalRegion_sigHist);
	signalRegion_sigList = binsToList( signalRegion_sigHist );
	signalRegion_tauList = textToList( "inputsHadTau/HadTauYieldsUnc10fb.txt", 0 );
	contributionsPerBin = [];
	for i in range(len(tagsForSignalRegion)): contributionsPerBin.append(['sig','WTopHadTau']);
	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)
	signalRegion_Rates = [];
	for i in range(signalRegion._nBins):
		tmpList = [];
		tmpList.append(signalRegion_sigList[i]);
		tmpList.append(signalRegion_tauList[i]);
		signalRegion_Rates.append( tmpList );
	signalRegion.fillRates( signalRegion_Rates );

	signalRegion.writeRates();

	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);
	hadtauSystematics = textToList( "inputsHadTau/HadTauMCPred10fb.txt",1 )
	hadtauClosureSystematics = {};
	hadtauClosureSystematics['NJets0'] = 1.2;
	hadtauClosureSystematics['NJets1'] = 1.4;
	hadtauClosureSystematics['NJets2'] = 1.6;

	for i in range(signalRegion.GetNbins()):
		njetTag = tagsForSignalRegion[i].split('_')[0];
		# print njetTag
		signalRegion.addSingleSystematic('HadTauUnc'+str(i),'lnN',['WTopHadTau'],float(hadtauSystematics[i]),'',i);
	
	signalRegion.addSingleSystematic('HadTauNJClosureNJets0Unc','lnN',['WTopHadTau'],hadtauClosureSystematics['NJets0'],'NJets0');
	signalRegion.addSingleSystematic('HadTauNJClosureNJets1Unc','lnN',['WTopHadTau'],hadtauClosureSystematics['NJets1'],'NJets1');
	signalRegion.addSingleSystematic('HadTauNJClosureNJets2Unc','lnN',['WTopHadTau'],hadtauClosureSystematics['NJets2'],'NJets2');
		
	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
