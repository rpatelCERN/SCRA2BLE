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
	signalRegion_statUncList = binsToList( LL_file.Get("fullStatUp_LL") );
	
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
	QCDcontributionsPerBinForSignal = [];
	QCDratiosPerContributionForSignal = [];
	QCDratesPerContributionForSignal = [];
	lowdphiRegion_sigHist = lowdphiRegion_file.Get("RA2bin_"+sms);
	tagsForLowDPhiRegion = binLabelsToList(lowdphiRegion_sigHist)
	contributionsPerBin = [];
	for i in range(len(tagsForLowDPhiRegion)): 
		curtag = tagsForLowDPhiRegion[i];
		qcdcurtag = 'qcd'+curtag.replace('_','');
		contributionsPerBin.append( [ 'sig',qcdcurtag ] );
	lowdphiRegion = searchRegion('lowdphi', contributionsPerBin, tagsForLowDPhiRegion)
	lowdphiRegion_sigList = binsToList(lowdphiRegion_sigHist);
	lowdphiRegion_qcdList = textToList('inputsFromOwen/lhbuilder-input-v4b-perfect-closure-ss1-fullfit-qcdcounts-%sifb.txt' % (str(int(lumi))) ,3);
	lowdphiRegion_Rates = [];
	QCDCRDict_TagToObs = {};
	QCDCRDict_TagToRate = {};
	for i in range(lowdphiRegion._nBins):
		curtag = tagsForLowDPhiRegion[i];
		qcdcurtag = 'qcd'+curtag.replace('_','');
		tmpList = [];
		tmpList.append(0.);
		tmpList.append(lowdphiRegion_qcdList[i]);
		QCDCRDict_TagToRate[qcdcurtag] = lowdphiRegion_qcdList[i]
		
		#print qcdcurtag
		QCDCRDict_TagToObs[qcdcurtag] = lowdphiRegion_qcdList[i]
		lowdphiRegion_Rates.append( tmpList );	

	HTDict  = { 'HT0':['HT0'], 'HT1':['HT1'], 'HT2':['HT2'], 'HT3':['HT0','HT1'], 'HT4':['HT2'], 'HT5':['HT1','HT2'] };
	MHTDict = { 'MHT0':['MHT0','MHT1'], 'MHT1':['MHT2'], 'MHT2':['MHT3'] };
	NJDict  = { 'NJets0':['NJets0','NJets1','NJets2'], 'NJets1':['NJets3'], 'NJets2':['NJets4'] };
	kappaHTDict  =  { 'HT0':0.062,'HT1':0.048,'HT2':0.036 }
	kappaMHTDict =  { 'MHT0':1.0,'MHT1':0.472,'MHT2':0.328,'MHT3':0.308 }
	kappaNJDict  =  { 'NJets0':1.0,'NJets1':1.45,'NJets2':1.45,'NJets3':2.11,'NJets4':4.0 }

	kappaUncMHTDict =  { 'MHT0':0.000,'MHT1':0.080,'MHT2':0.16,'MHT3':0.30 }
	kappaUncNJDict  =  { 'NJets0':0.0000,'NJets1':0.015,'NJets2':0.15,'NJets3':0.30,'NJets4':2.0}
	kappaUncHTDict  =  { 'HT0':0.01,'HT1':0.008,'HT2':0.006 }

	TotalLowdphiRegion_Rates = [];
	for i in range(len(tagsForSignalRegion)):
		curtag = tagsForSignalRegion[i];
		curtaglist = curtag.split('_');
		translatedBins = [];
		translatedBins.append('sig');
		kappaRatios = [];
		ratesFromKappas = [];
		tmp=0;
		tmp2=0;
		for val0 in NJDict[curtaglist[0]]:
			for val1 in MHTDict[curtaglist[2]]:
				for val2 in HTDict[curtaglist[3]]:
					qcdlookupkey='qcd'+val0+curtaglist[1]+val1+val2;
					tmp=kappaNJDict[val0]*kappaMHTDict[val1]*kappaHTDict[val2]*QCDCRDict_TagToRate[qcdlookupkey]+tmp;
					tmp2=QCDCRDict_TagToRate[qcdlookupkey]+tmp2
					#curratio = kappaNJDict[val0]*kappaMHTDict[val1]*kappaHTDict[val2];
					#print qcdkey
					#cursignalyield = curratio*QCDCRDict_TagToRate[qcdkey];
					#print QCDCRDict_TagToRate[qcdkey]
		#print " bin %d  qcd yield  %2.2f" %(i, tmp)
		translatedBins.append('qcd');
		kappaRatios.append( tmp )
		ratesFromKappas.append( tmp );
		QCDcontributionsPerBinForSignal.append( translatedBins );
		QCDratiosPerContributionForSignal.append( tmp );
		QCDratesPerContributionForSignal.append( tmp );
		TotalLowdphiRegion_Rates.append(tmp2);
	
	NewControlRegion = searchRegion('Lowdphi', QCDcontributionsPerBinForSignal, tagsForSignalRegion);	

	signalRegion_Rates = [];
	signalRegion_Observed = [];
	controlRegion_Rates = [];
	controllRegion_Observed = [];
	for i in range(NewControlRegion._nBins):
		curobsC = 0;
		currateC = [];
		currateC.append(0)
		currateC.append(TotalLowdphiRegion_Rates[i]);
		curobsC += TotalLowdphiRegion_Rates[i]
		controlRegion_Rates.append(currateC);
		controllRegion_Observed.append(curobsC);	
	NewControlRegion.fillRates(controlRegion_Rates);
	NewControlRegion.setObservedManually(controllRegion_Observed);
	NewControlRegion.writeRates();

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
		if options.allBkgs or options.qcdOnly: srobs += QCDratesPerContributionForSignal[i];
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
		if options.allBkgs or options.qcdOnly: tmpList.append( QCDratesPerContributionForSignal[i] );
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
			
			# print signalRegion_CSList[i], denom, signalRegion_WeightList[i], signalRegion_sysUncList[i], signalRegion_statUncList[i]

		for i in range(SLcontrolRegion.GetNbins()):
			SLcontrolRegion.addSingleSystematic('LLSCSR'+tagsForSLControlRegion[i],'lnU',['WTopSL'],100,'',i);		

	### hadtau uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.tauOnly:
		
		for i in range(signalRegion.GetNbins()):
			njetTag = tagsForSignalRegion[i].split('_')[0];
			# print njetTag
			signalRegion.addSingleSystematic('LLStat'+tagsForSignalRegion[i],'lnN',['WTopHad'],float(hadtauSystematics[i]),'',i);
		
		signalRegion.addSingleSystematic('HadTauNJClosureNJets0Unc','lnN',['WTopHad'],1.2,'NJets0');
		signalRegion.addSingleSystematic('HadTauNJClosureNJets1Unc','lnN',['WTopHad'],1.4,'NJets1');
		signalRegion.addSingleSystematic('HadTauNJClosureNJets2Unc','lnN',['WTopHad'],1.6,'NJets2');

	### QCD uncertainties ------------------------------------------------------------------------------
	if options.allBkgs or options.qcdOnly:	
		logNormalUnc=[]
		for i in range(len(tagsForSignalRegion)):
			curtag = tagsForSignalRegion[i];
			curtaglist = curtag.split('_');
			translatedBins = [];
			translatedBins.append('sig');
			sumQCDQuad=0;		
			for val0 in NJDict[curtaglist[0]]:
				for val1 in MHTDict[curtaglist[2]]:
					for val2 in HTDict[curtaglist[3]]:
						qcdlookupkey='qcd'+val0+curtaglist[1]+val1+val2;
						qcdNJUncRatio=kappaUncNJDict[val0]/kappaNJDict[val0]
						qcdHTUncRatio=kappaUncHTDict[val2]/kappaHTDict[val2]
						qcdMHTUncRatio=kappaUncMHTDict[val1]/kappaMHTDict[val1]
						qcdControlYield=QCDCRDict_TagToRate[qcdlookupkey]
						sumquad=(qcdNJUncRatio*qcdNJUncRatio)+(qcdHTUncRatio*qcdHTUncRatio)+(qcdMHTUncRatio*qcdMHTUncRatio)
						sumQCDQuad+=(sqrt(sumquad)*qcdControlYield)

			den=TotalLowdphiRegion_Rates[i]
			if(den<0.000001):den=1.0
			unc=1+((sumQCDQuad)/den)
			logNormalUnc.append(unc)

		for i in range(signalRegion._nBins):
			sysLN="Logqcd%d" %i
			sysLNU="Ratioqcd%d" %i
			signalRegion.addSingleSystematic(sysLNU,'lnU','qcd',100,'',i);
			signalRegion.addSingleSystematic(sysLN,'lnN','qcd',logNormalUnc[i],'',i);
			NewControlRegion.addSingleSystematic(sysLNU,'lnU','qcd',100,'',i);	

	# #------------------------------------------------------------------------------------------------
	# ## 3. Write Cards
	signalRegion.writeCards( odir );
	if options.allBkgs or options.llpOnly: SLcontrolRegion.writeCards( odir );
	if options.allBkgs or options.tauOnly: HadcontrolRegion.writeCards( odir );
	if options.allBkgs or options.zvvOnly: sphotonRegion.writeCards( odir );
	if options.allBkgs or options.qcdOnly: NewControlRegion.writeCards( odir );



