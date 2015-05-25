from ROOT import *

import math
import sys
from searchRegion import *
from singleBin import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option("--lumi", dest="lumi", default = 4,help="mass of LSP", metavar="MLSP")
parser.add_option("--binning",dest="binning",default="RA2bBins",help="Select binning to be used: Classic, SMJ, extSMJ", metavar="binning")
(options, args) = parser.parse_args()


#########################################################################################################
#########################################################################################################
if __name__ == '__main__':

	odir = 'testCards/';

	#------------------------------------------------------------------------------------------------
	## 1. Fill Rates for each signal region
	signalRegion_file = TFile("../Analysis/datacards/RA2bin_signal.root");
	signalRegion_hists = [];
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_SMStttt1500") );
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_QCD") );
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_Zinv") );
	signalRegion_hists.append( signalRegion_file.Get("RA2bin_WJet") );
	signalRegion = searchRegion('signal', ['sig','qcd','zvv','wjttb'], signalRegion_hists[0])
	signalRegion.fillRates( signalRegion_hists );

	lostlepRegion_file = TFile("../Analysis/datacards/RA2bin_SL.root");
	lostlepRegion_hists = [];
	lostlepRegion_hists.append( lostlepRegion_file.Get("RA2bin_SMStttt1500") );
	lostlepRegion_hists.append( lostlepRegion_file.Get("RA2bin_QCD") );
	lostlepRegion_hists.append( lostlepRegion_file.Get("RA2bin_Zinv") );
	lostlepRegion_hists.append( lostlepRegion_file.Get("RA2bin_WJet") );
	lostlepRegion = searchRegion('lostlep', ['sig','qcd','zvv','wjttb'], lostlepRegion_hists[0])
	lostlepRegion.fillRates( lostlepRegion_hists );

	lowdphiRegion_file = TFile("../Analysis/datacards/RA2bin_LDP.root");
	lowdphiRegion_hists = [];
	lowdphiRegion_hists.append( lowdphiRegion_file.Get("RA2bin_SMStttt1500") );
	lowdphiRegion_hists.append( lowdphiRegion_file.Get("RA2bin_QCD") );
	lowdphiRegion_hists.append( lowdphiRegion_file.Get("RA2bin_Zinv") );
	lowdphiRegion_hists.append( lowdphiRegion_file.Get("RA2bin_WJet") );
	lowdphiRegion = searchRegion('lowdphi', ['sig','qcd','zvv','wjttb'], lowdphiRegion_hists[0])
	lowdphiRegion.fillRates( lowdphiRegion_hists );

	sphotonRegion_file = TFile("../Analysis/datacards/RA2bin_GJet_NoPhotonVars.root");
	sphotonRegion_hists = [];
	sphotonRegion_hists.append( sphotonRegion_file.Get("RA2bin_SMStttt1500") );
	sphotonRegion_hists.append( sphotonRegion_file.Get("RA2bin_QCD") );
	sphotonRegion_hists.append( sphotonRegion_file.Get("RA2bin_GJet") );
	sphotonRegion_hists.append( sphotonRegion_file.Get("RA2bin_WJet") );
	sphotonRegion = searchRegion('sphoton', ['sig','qcd','zvv','wjttb'], sphotonRegion_hists[0])
	sphotonRegion.fillRates( sphotonRegion_hists );

	#------------------------------------------------------------------------------------------------
	## 2. Add systematics
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);
	signalRegion.addSingleSystematic('LostLepRatUnc','lnN',['wjttb'],1.30);
	signalRegion.addSingleSystematic('LDPRatUnc','lnN',['qcd'],1.30);
	signalRegion.addSingleSystematic('SPhoRatUnc','lnN',['zvv'],1.30,'BTags0');

	for i in range(signalRegion.GetNbins()):

		# connect the lost lepton CR to the signal region
		signalRegion.addSingleSystematic('LostLepCR'+str(i),'lnU',['wjttb'],100,'',i);
		lostlepRegion.addSingleSystematic('LostLepCR'+str(i),'lnU',['wjttb'],100,'',i);

		# connect the low deltaPhi CR to the signal region
		signalRegion.addSingleSystematic('LDPCR'+str(i),'lnU',['qcd'],100,'',i);
		lowdphiRegion.addSingleSystematic('LDPCR'+str(i),'lnU',['qcd'],100,'',i);

	# connect the single photon CR to the signal region
	singlePhotonBins = ["NJets0_BTags0_MHT0_HT0","NJets0_BTags0_MHT0_HT1","NJets0_BTags0_MHT0_HT2","NJets0_BTags0_MHT1_HT3","NJets0_BTags0_MHT1_HT4","NJets0_BTags0_MHT2_HT5",
						"NJets1_BTags0_MHT0_HT0","NJets1_BTags0_MHT0_HT1","NJets1_BTags0_MHT0_HT2","NJets1_BTags0_MHT1_HT3","NJets1_BTags0_MHT1_HT4","NJets1_BTags0_MHT2_HT5",
						"NJets2_BTags0_MHT0_HT0","NJets2_BTags0_MHT0_HT1","NJets2_BTags0_MHT0_HT2","NJets2_BTags0_MHT1_HT3","NJets2_BTags0_MHT1_HT4","NJets2_BTags0_MHT2_HT5"];
	
	for i in range(len(singlePhotonBins)):
		signalRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);
		sphotonRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],100,singlePhotonBins[i]);

	# connect the 0B bins to nB bins
	signalRegion.addSingleSystematic('DYRatUnc','lnN',['zvv'],1.3,'BTags1');
	signalRegion.addSingleSystematic('DYRatUnc','lnN',['zvv'],1.3,'BTags2');
	signalRegion.addSingleSystematic('DYRatUnc','lnN',['zvv'],1.3,'BTags3');
	signalRegion.addSingleSystematic('DYCR0BTo1B','lnU',['zvv'],100,'BTags1');
	signalRegion.addSingleSystematic('DYCR0BTo1B','lnU',['zvv'],100,'BTags0');
	signalRegion.addSingleSystematic('DYCR0BTo2B','lnU',['zvv'],100,'BTags2');
	signalRegion.addSingleSystematic('DYCR0BTo2B','lnU',['zvv'],100,'BTags0');
	signalRegion.addSingleSystematic('DYCR0BTo3B','lnU',['zvv'],100,'BTags3');
	signalRegion.addSingleSystematic('DYCR0BTo3B','lnU',['zvv'],100,'BTags0');

	#------------------------------------------------------------------------------------------------
	## 3. Write Cards
	signalRegion.writeCards( odir );
	lostlepRegion.writeCards( odir );	
	lowdphiRegion.writeCards( odir );	
	sphotonRegion.writeCards( odir );	
