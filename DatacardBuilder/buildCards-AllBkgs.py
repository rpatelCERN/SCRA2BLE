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

parser.add_option('--qcdOnly', action='store_true', dest='qcdOnly', default=False, help='no X11 windows')
parser.add_option('--zvvOnly', action='store_true', dest='zvvOnly', default=False, help='no X11 windows')
parser.add_option('--tauOnly', action='store_true', dest='tauOnly', default=False, help='no X11 windows')
parser.add_option('--llpOnly', action='store_true', dest='llpOnly', default=False, help='no X11 windows')
parser.add_option('--allBkgs', action='store_true', dest='allBkgs', default=False, help='no X11 windows')

(options, args) = parser.parse_args()


#########################################################################################################
## to do:
## 1. put in asymmetric uncertainties from Jim/Arne(?)
## 2. add the new uncertainty scheme from Owen
## 3. try the hardcore QCD background estimate; also include lost lepton
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
	lowdphiRegion_file = TFile(idir+"/RA2bin_LDP.root");

	# signal --------
	signalRegion_sigHist = signalRegion_file.Get("RA2bin_"+sms);
	tagsForSignalRegion = binLabelsToList(signalRegion_sigHist);
	signalRegion_sigList = binsToList( signalRegion_sigHist );

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
	
	# print  "./inputsLostLepton/statunc%sfb.txt" % (str(int(lumi)))
	signalRegion_statUncList = textToList( "./inputsLostLepton/statunc%sfb.txt" % (str(int(lumi))), 0 );
	signalRegion_sysUncList = textToList( "./inputsLostLepton/sysunc%sfb.txt" % (str(int(lumi))), 0 );

	# had tau
	signalRegion_tauList = textToList( "inputsHadTau/HadTauMCPred%sfb.txt" % (str(int(lumi))), 0 );
	hadtauSystematics = textToList( "inputsHadTau/HadTauMCPred%sfb.txt" % (str(int(lumi))), 1 )
	controlRegion_tauList = textToList( "inputsHadTau/TauControlBins%sfb.txt" % (str(int(lumi))), 0 );
	#for i in range(len(controlRegion_tauList)):
	#	if(controlRegion_tauList[i]<2):print controlRegion_tauList[i]
	
	# QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ
	# QCD stuff
	# low dphi region stuff

	ratesForSignalRegion_QCDList = [];
	NSRForSignalRegion_QCDList = textToList("inputsFromOwen/lowdphiinputs-72bins-%sifb.txt"%(str(int(lumi))),4);
	ratesForLowdphiRegion_QCDList = [];
	NCRForLowdphiRegion_QCDList = textToList("inputsFromOwen/lowdphiinputs-72bins-%sifb.txt"%(str(int(lumi))),2);
	obsForLowdphiRegion_QCDList = [];
	ratiosForLowdphiRegion = textToList("inputsFromOwen/lowdphiinputs-72bins-%sifb.txt"%(str(int(lumi))),3);

	lowdphiRegion_sigHist = lowdphiRegion_file.Get("RA2bin_"+sms);
	ratesForLowdphiRegion_sigList = binsToList(lowdphiRegion_sigHist);
	tagsForLowDPhiRegion = binLabelsToList(lowdphiRegion_sigHist)
	QCDcontributionsPerBin = [];
	for i in range(len(tagsForLowDPhiRegion)): 
		QCDcontributionsPerBin.append( [ 'sig','qcd' ] );

		if NCRForLowdphiRegion_QCDList[i] < 1: 
			ratesForLowdphiRegion_QCDList.append( 1. );
			ratesForSignalRegion_QCDList.append( ratiosForLowdphiRegion[i] )
		else: 
			ratesForLowdphiRegion_QCDList.append( NCRForLowdphiRegion_QCDList[i] ); 
			ratesForSignalRegion_QCDList.append( NSRForSignalRegion_QCDList[i] )

		#obsForLowdphiRegion_QCDList.append( NCRForLowdphiRegion_QCDList[i] + ratesForLowdphiRegion_sigList[i])
		obsForLowdphiRegion_QCDList.append( NCRForLowdphiRegion_QCDList[i] ); # currently not considering signal contamination

	LowdphiControlRegion = searchRegion('Lowdphi', QCDcontributionsPerBin, tagsForLowDPhiRegion);	
	qcdcontrolRegion_Rates = [];
	qcdcontrollRegion_Observed = [];
	for i in range(LowdphiControlRegion._nBins):
		curobsC = 0;
		curobsC += obsForLowdphiRegion_QCDList[i]		

		currateC = [];
		currateC.append( 0. );
		currateC.append( ratesForLowdphiRegion_QCDList[i] );
	
		qcdcontrolRegion_Rates.append(currateC);
		qcdcontrollRegion_Observed.append(curobsC);	

	LowdphiControlRegion.fillRates(qcdcontrolRegion_Rates);
	LowdphiControlRegion.setObservedManually(qcdcontrollRegion_Observed);
	LowdphiControlRegion.writeRates();

	# QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ

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

	# accounting for LL Region
	tagsForSLControlRegion=[]	
	tagsForHadControlRegion=[]
	SLcontrolContributionsPerBin = [];
	HadcontrolContributionsPerBin=[]	
	addControl=[]
	addControlHad=[]
	for i in range(len(tagsForSignalRegion)): 
		if(signalRegion_CSList[i]<2):
			SLcontrolContributionsPerBin.append(['sig', 'WTopSL']);
			tagsForSLControlRegion.append(tagsForSignalRegion[i]);
			addControl.append(i);
		if(controlRegion_tauList[i]<2):
			HadcontrolContributionsPerBin.append(['sig', 'WTopHad']);
			addControlHad.append(i);
			tagsForHadControlRegion.append(tagsForSignalRegion[i])
	SLcontrolRegion = searchRegion('SLControl', SLcontrolContributionsPerBin, tagsForSLControlRegion)
	HadcontrolRegion = searchRegion('HadControl', HadcontrolContributionsPerBin, tagsForHadControlRegion)
	SLcontrolRegion_Obs = [];
	SLcontrolRegion_Rates = [];
	HadcontrolRegion_Obs = [];
	HadcontrolRegion_Rates = [];
	for i in range(len(addControl)):
		tmpList=[]
		tmpList.append(0);
		tmpList.append(1.);
		SLcontrolRegion_Obs.append(signalRegion_CSList[addControl[i]]);
		SLcontrolRegion_Rates.append(tmpList);
		for i in range(len(addControlHad)):
			tmpList2=[]
			tmpList2.append(0);
			tmpList2.append(1.);
			HadcontrolRegion_Obs.append(controlRegion_tauList[addControlHad[i]]);
			HadcontrolRegion_Rates.append(tmpList2);
		
	SLcontrolRegion.fillRates(SLcontrolRegion_Rates);
	SLcontrolRegion.setObservedManually(SLcontrolRegion_Obs);
	HadcontrolRegion.fillRates(HadcontrolRegion_Rates);
	HadcontrolRegion.setObservedManually(HadcontrolRegion_Obs);
		
	# -------------------------------
	# signal region
	contributionsPerBin = [];
	for i in range(len(tagsForSignalRegion)): 
		tmpcontributions = [];
		tmpcontributions.append('sig');
		if options.allBkgs or options.llpOnly: tmpcontributions.append('WTopSL');
		if options.allBkgs or options.tauOnly: tmpcontributions.append('WTopHad');
		if options.allBkgs or options.zvvOnly: tmpcontributions.append('zvv');
		if options.allBkgs or options.qcdOnly: tmpcontributions.append('qcd');
		contributionsPerBin.append(tmpcontributions);

	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)

	signalRegion_Rates = [];
	signalRegion_Obs = [];
	controlRegion_Rates=[];

	for i in range(signalRegion._nBins):
		srobs = 0;
		srobs += signalRegion_sigList[i]*signalmu;
		if options.allBkgs or options.qcdOnly: srobs += NSRForSignalRegion_QCDList[i];
		if options.allBkgs or options.zvvOnly: srobs += signalRegion_zvvList[i];
		if options.allBkgs or options.llpOnly: srobs += signalRegion_LLList[i];
		if options.allBkgs or options.tauOnly: srobs += signalRegion_tauList[i];
		signalRegion_Obs.append( srobs );

		tmpList = [];
		tmpList.append(signalRegion_sigList[i]);

		# LL rate
		if options.allBkgs or options.llpOnly:		
			
			if(signalRegion_CSList[i]>=2):
				tmpList.append(signalRegion_LLList[i]);
			else:
				tmpList.append(signalRegion_WeightList[i]); # the control region "rate" line is always going to be 1
				addControl.append(i);

		# Had Tau rate
		if options.allBkgs or options.tauOnly: tmpList.append(signalRegion_tauList[i]);
		if options.allBkgs or options.zvvOnly: tmpList.append(signalRegion_zvvList[i]);
		if options.allBkgs or options.qcdOnly: tmpList.append( ratesForSignalRegion_QCDList[i] );
		signalRegion_Rates.append( tmpList );
	
	signalRegion.fillRates( signalRegion_Rates );
	signalRegion.setObservedManually(signalRegion_Obs)

	SLcontrolRegion.writeRates();
	sphotonRegion.writeRates();
	signalRegion.writeRates();

	# #------------------------------------------------------------------------------------------------
	# #------------------------------------------------------------------------------------------------
	# #------------------------------------------------------------------------------------------------
	# #------------------------------------------------------------------------------------------------
	# ## 2. Add systematics
	signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.04);
	signalRegion.addSingleSystematic('EvtFilters','lnN',['sig'],1.03);
	signalRegion.addSingleSystematic('PUwUnc','lnN',['sig'],1.03);
	signalRegion.addSingleSystematic('TrigEff','lnN',['sig'],1.02);
	
	### Zvv uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.zvvOnly:
		
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
			signalRegion.addSingleSystematic('SPhoRZgUnc'+str(i),'lnN',['zvv'],RzgammaUnc[i],'',i);
		for i in range(18,72): # only for the 0B bins
			signalRegion.addSingleSystematic('DYHTUnc'+str(i),'lnN',['zvv'],1.20,'',i);

		# added to all bins (photon efficiency)
		signalRegion.addSingleSystematic('PhoEffUnc','lnN',['zvv'],1.2,'NJets');	

		if lumi == 10.0:
			#RZg data/MC double ratios from Jim H.
			signalRegion.addSingleSystematic('RZgDataUncMHT0','lnN',['zvv'],1.04,'MHT0');	
			signalRegion.addSingleSystematic('RZgDataUncMHT1','lnN',['zvv'],1.11,'MHT1');	
			signalRegion.addSingleSystematic('RZgDataUncMHT2','lnN',['zvv'],1.28,'MHT2');	
			signalRegion.addSingleSystematic('RZgDataUncNJets0','lnN',['zvv'],1.06,'NJets0');	
			signalRegion.addSingleSystematic('RZgDataUncNJets1','lnN',['zvv'],1.13,'NJets1');	
			signalRegion.addSingleSystematic('RZgDataUncNJets2','lnN',['zvv'],1.16,'NJets2');				
			# Extrpolation uncertainties, from Kevin S.
			signalRegion.addSingleSystematic('DYNBStatUncBTags1','lnN',['zvv'],1.076,'BTags1');		
			signalRegion.addSingleSystematic('DYNBStatUncBTags2','lnN',['zvv'],1.158,'BTags2');		
			signalRegion.addSingleSystematic('DYNBStatUncBTags3','lnN',['zvv'],1.507,'BTags3');		
			signalRegion.addSingleSystematic('DYNBStatUncNJets1','lnN',['zvv'],1.008,'NJets1_BTags.');		
			signalRegion.addSingleSystematic('DYNBStatUncNJets2','lnN',['zvv'],1.049,'NJets2_BTags.');		
		
		if lumi == 3.0:
			#RZg data/MC double ratios from Jim H.
			signalRegion.addSingleSystematic('RZgDataUncMHT0','lnN',['zvv'],1.08,'MHT0');	
			signalRegion.addSingleSystematic('RZgDataUncMHT1','lnN',['zvv'],1.21,'MHT1');	
			signalRegion.addSingleSystematic('RZgDataUncMHT2','lnN',['zvv'],1.54,'MHT2');	
			signalRegion.addSingleSystematic('RZgDataUncNJets0','lnN',['zvv'],1.12,'NJets0');	
			signalRegion.addSingleSystematic('RZgDataUncNJets1','lnN',['zvv'],1.25,'NJets1');	
			signalRegion.addSingleSystematic('RZgDataUncNJets2','lnN',['zvv'],1.32,'NJets2');				
			# Extrpolation uncertainties, from Kevin S.
			signalRegion.addSingleSystematic('DYNBStatUncBTags1','lnN',['zvv'],1.076,'BTags1');		
			signalRegion.addSingleSystematic('DYNBStatUncBTags2','lnN',['zvv'],1.158,'BTags2');		
			signalRegion.addSingleSystematic('DYNBStatUncBTags3','lnN',['zvv'],1.507,'BTags3');		
			signalRegion.addSingleSystematic('DYNBStatUncNJets1','lnN',['zvv'],1.015,'NJets1_BTags.');		
			signalRegion.addSingleSystematic('DYNBStatUncNJets2','lnN',['zvv'],1.059,'NJets2_BTags.');		


	### LL uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.llpOnly:

		for i in range(signalRegion.GetNbins()):
			denom = signalRegion_LLList[i]
			if(signalRegion_CSList[i]<2):
				signalRegion.addSingleSystematic('LLSCSR'+tagsForSignalRegion[i],'lnU',['WTopSL'],100,'',i);
			else: 
				signalRegion.addSingleSystematic('LLStat'+tagsForSignalRegion[i],'lnN',['WTopSL'],1+(signalRegion_statUncList[i]/denom),'',i);					
			if(signalRegion_LLList[i]<0.00001): denom = signalRegion_WeightList[i]
			signalRegion.addSingleSystematic('LLSys'+tagsForSignalRegion[i],'lnN',['WTopSL'],1+(signalRegion_sysUncList[i]/denom),'',i);
			
		for i in range(SLcontrolRegion.GetNbins()):
			SLcontrolRegion.addSingleSystematic('LLSCSR'+tagsForSLControlRegion[i],'lnU',['WTopSL'],100,'',i);		

	### hadtau uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.tauOnly:
		
		for i in range(signalRegion.GetNbins()):
			njetTag = tagsForSignalRegion[i].split('_')[0];
			# print njetTag
			signalRegion.addSingleSystematic('HadStat'+tagsForSignalRegion[i],'lnN',['WTopHad'],float(hadtauSystematics[i]),'',i);
			#addMultiSystematic('HadStat'+tagsForSignalRegion[i],'lnN',['WTopSL','WTopHad'],[float(hadtauSystematics[i]),1],'',i);
		signalRegion.addSingleSystematic('HadTauNJClosureNJets0Unc','lnN',['WTopHad'],1.2,'NJets0');
		signalRegion.addSingleSystematic('HadTauNJClosureNJets1Unc','lnN',['WTopHad'],1.4,'NJets1');
		signalRegion.addSingleSystematic('HadTauNJClosureNJets2Unc','lnN',['WTopHad'],1.6,'NJets2');

	### QCD uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.qcdOnly:	

		ListOfQCDSys = getSystematicsListQCD("inputsFromOwen/lowdphiinputs-72bins-%sifb.txt"%(str(int(lumi))));
		
		for i in range(len(tagsForSignalRegion)):
			signalRegion.addSingleSystematic(        "ldpCR"+str(i),'lnU','qcd',100,'',i);
			LowdphiControlRegion.addSingleSystematic("ldpCR"+str(i),'lnU','qcd',100,'',i);	

			for sys in ListOfQCDSys[i]:
				signalRegion.addSingleSystematic("kappaUnc"+sys[0],'lnN','qcd',float(sys[1]),'',i);

	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
	if options.allBkgs or options.llpOnly: SLcontrolRegion.writeCards( odir );
	if options.allBkgs or options.tauOnly: HadcontrolRegion.writeCards( odir );
	if options.allBkgs or options.zvvOnly: sphotonRegion.writeCards( odir );
	if options.allBkgs or options.qcdOnly: LowdphiControlRegion.writeCards( odir );



