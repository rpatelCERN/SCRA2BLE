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
parser.add_option('--fastsim', action='store_true', dest='fastsim', default=False, help='no X11 windows')
parser.add_option('--realData', action='store_true', dest='realData', default=False, help='no X11 windows')

parser.add_option('--qcdOnly', action='store_true', dest='qcdOnly', default=False, help='no X11 windows')
parser.add_option('--zvvOnly', action='store_true', dest='zvvOnly', default=False, help='no X11 windows')
parser.add_option('--tauOnly', action='store_true', dest='tauOnly', default=False, help='no X11 windows')
parser.add_option('--llpOnly', action='store_true', dest='llpOnly', default=False, help='no X11 windows')
parser.add_option('--allBkgs', action='store_true', dest='allBkgs', default=False, help='no X11 windows')
parser.add_option("--mGo", dest="mGo", default='1000', help="Mass of Gluino", metavar="mGo")
parser.add_option("--mLSP", dest="mLSP", default='900', help="Mass of LSP", metavar="mLSP")
(options, args) = parser.parse_args()


#########################################################################################################
## to do:
## .......
#########################################################################################################
if __name__ == '__main__':

	sms = "mGluino"+options.mGo;
	tag = options.tag;
	lumi = float(options.lumi);
	signalmu = float(options.mu);
	odir = 'testCards-%s-T5HH%s-%1.1f-mu%0.1f/' % ( tag,sms, lumi, signalmu );
	#idir = 'inputHistograms/histograms_%1.1ffb/' % ( ((lumi)) );
	if os.path.exists(odir): os.system( "rm -rf %s" % (odir) );
	os.makedirs(odir);
	idir="./"
	#print odir, signalmu

	######################################################################
	######################################################################
	## 1. Get the input histograms from each of the background teams
	######################################################################
	######################################################################

	# --------------------------------------------
	# signal 
	signaldirtag = idir;
	parse=sms.split('_')
	model=parse[0]
	#print parse
	Datacards_file =TFile(signaldirtag+"datacardInputs.root");
	#signal region
	print "AnalysisBins_SR_singleHiggsTag_%s" %sms
					
	signalHiggs=Datacards_file.Get("AnalysisBins_SR_singleHiggsTag_%s" %sms)
	signal=binsToList(signalHiggs)
	SRWJets=Datacards_file.Get("AnalysisBins_SR_singleHiggsTag_WJets");
        SRW=binsToList(SRWJets)
	SRTTBar=Datacards_file.Get("AnalysisBins_SR_singleHiggsTag_TT");
	SRTT=binsToList(SRTTBar)
	SRZJets=Datacards_file.Get("AnalysisBins_SR_singleHiggsTag_ZJets");
	SRZ=binsToList(SRZJets)
	SRQCD=Datacards_file.Get("AnalysisBins_SR_singleHiggsTag_QCD");
	SRQcd=binsToList(SRQCD)
	tagsForSignalRegion = binLabelsToList(signalHiggs);
	contributionsPerBin=[]
 	for i in range(len(tagsForSignalRegion)): 
		tmpcontributions = [];
		tmpcontributions.append('sig'); 
		tmpcontributions.append('WJets'); 
		tmpcontributions.append('TTbar'); 
		tmpcontributions.append('ZJets');
		tmpcontributions.append('QCD');
		contributionsPerBin.append( tmpcontributions)
	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)	
	signalRegion_Rates = [];
	signalRegion_Obs = [];
	f = TFile(odir+'yields.root', 'recreate')
	data = TH1F( 'data', 'data', 8, 0, 8 )
	qcd = TH1F( 'QCD', 'QCD', 8, 0, 8 )
	zvv = TH1F( 'Zvv', 'Zvv', 8, 0, 8 )
	WJ = TH1F( 'WJ', 'WJ', 8, 0, 8 )
	TT = TH1F( 'TT', 'TT', 8, 0, 8 )
	sig = TH1F( 'sig', 'sig', 8, 0, 8 )
	for i in range(signalRegion._nBins):
		tmpList=[]
		tmpList.append(signal[i])
		tmpList.append(SRW[i])
		tmpList.append(SRTT[i])
		tmpList.append(SRZ[i])
		tmpList.append(SRQcd[i])
		signalRegion_Rates.append( tmpList );
		srobs=SRW[i]+SRTT[i]+SRZ[i]+SRQcd[i]
		data.Fill(i+.5, srobs)
		qcd.Fill(i+.5,SRQcd[i])
		zvv.Fill(i+.5, SRZ[i])
		TT.Fill(i+.5,SRTT[i])
		WJ.Fill(i+.5,SRW[i])
		sig.Fill(i+.5, signal[i])
		signalRegion_Obs.append( srobs );
	signalRegion.setObservedManually(signalRegion_Obs);
	signalRegion.fillRates(signalRegion_Rates );
	signalRegion.writeRates();
        f.Write()
        f.Close()
	#AntiTag Region
	AntitagSignalCont=Datacards_file.Get("AnalysisBins_SR_antiTag_%s" %sms)
	Antitagsig=binsToList(AntitagSignalCont)
	AntitagWJets=Datacards_file.Get("AnalysisBins_SR_antiTag_WJets");
        AntitagW=binsToList(AntitagWJets)
	AntitagTTBar=Datacards_file.Get("AnalysisBins_SR_antiTag_TT");
	AntitagTT=binsToList(AntitagTTBar)
	AntitagZJets=Datacards_file.Get("AnalysisBins_SR_antiTag_ZJets");
	AntitagZ=binsToList(AntitagZJets)
	AntitagQCD=Datacards_file.Get("AnalysisBins_SR_antiTag_QCD");
	AntitagQcd=binsToList(AntitagQCD)
	contributionsPerBin=[]
	for i in range(len(tagsForSignalRegion)):
                tmpcontributions = [];
                tmpcontributions.append('sig');
                tmpcontributions.append('WJets');
                tmpcontributions.append('TTbar');
                tmpcontributions.append('ZJets');
                tmpcontributions.append('QCD');
                contributionsPerBin.append( tmpcontributions)
        AntiTagRegion = searchRegion('antitag', contributionsPerBin, tagsForSignalRegion)	
	AntiTagRegion_Rates = [];
        AntiTagRegion_Obs = [];
	for i in range(AntiTagRegion._nBins):
		tmpList=[]
                tmpList.append(Antitagsig[i])#include contamination in control bins!
                tmpList.append(AntitagW[i])
                tmpList.append(AntitagTT[i])
                tmpList.append(AntitagZ[i])
                tmpList.append(AntitagQcd[i])
		antitagobs=AntitagW[i]+AntitagTT[i]+AntitagZ[i]+AntitagQcd[i]
		AntiTagRegion_Rates.append(tmpList);
		AntiTagRegion_Obs.append(antitagobs)
	AntiTagRegion.fillRates(signalRegion_Rates);
	AntiTagRegion.writeRates()
        AntiTagRegion.setObservedManually(AntiTagRegion_Obs);

	#SideBand Region
	SidebandSignalCont=Datacards_file.Get("AnalysisBins_SB_singleHiggsTag_%s" %sms)
	Sidebandsig=binsToList(SidebandSignalCont)
	SidebandWJets=Datacards_file.Get("AnalysisBins_SB_singleHiggsTag_WJets");
        SidebandW=binsToList(SidebandWJets)
	SidebandTTBar=Datacards_file.Get("AnalysisBins_SB_singleHiggsTag_TT");
	SidebandTT=binsToList(SidebandTTBar)
	SidebandZJets=Datacards_file.Get("AnalysisBins_SB_singleHiggsTag_ZJets");
	SidebandZ=binsToList(SidebandZJets)
	SidebandQCD=Datacards_file.Get("AnalysisBins_SB_singleHiggsTag_QCD");
	SidebandQcd=binsToList(SidebandQCD)
	contributionsPerBin=[]
	for i in range(len(tagsForSignalRegion)):
                tmpcontributions = [];
                tmpcontributions.append('sig');
                tmpcontributions.append('WJets');
                tmpcontributions.append('TTbar');
                tmpcontributions.append('ZJets');
                tmpcontributions.append('QCD');
                contributionsPerBin.append( tmpcontributions)
        SideBandRegion = searchRegion('sideband', contributionsPerBin, tagsForSignalRegion)	
	SideBandRegion_Rates = [];
        SideBandRegion_Obs = [];
	for i in range(SideBandRegion._nBins):
		tmpList=[]
                tmpList.append(SidebandSignalCont[i])#include contamination in control bins!
                tmpList.append(SidebandW[i])
                tmpList.append(SidebandTT[i])
                tmpList.append(SidebandZ[i])
                tmpList.append(SidebandQcd[i])
		sidebandobs=SidebandW[i]+SidebandTT[i]+SidebandZ[i]+SidebandQcd[i]
		SideBandRegion_Rates.append(tmpList);
		SideBandRegion_Obs.append(sidebandobs)
	SideBandRegion.fillRates(signalRegion_Rates);
	SideBandRegion.writeRates()
        SideBandRegion.setObservedManually(SideBandRegion_Obs);
	#Sideband+Antitag region

	SidebandAntitagSignalCont=Datacards_file.Get("AnalysisBins_SB_antiTag_%s" %sms)
	SidebandAntitagsig=binsToList(SidebandAntitagSignalCont)
	SidebandAntitagWJets=Datacards_file.Get("AnalysisBins_SB_antiTag_WJets");
        SidebandAntitagW=binsToList(SidebandAntitagWJets)
	SidebandAntitagTTBar=Datacards_file.Get("AnalysisBins_SB_antiTag_TT");
	SidebandAntitagTT=binsToList(SidebandAntitagTTBar)
	SidebandAntitagZJets=Datacards_file.Get("AnalysisBins_SB_antiTag_ZJets");
	SidebandAntitagZ=binsToList(SidebandAntitagZJets)
	SidebandAntitagQCD=Datacards_file.Get("AnalysisBins_SB_antiTag_QCD");
	SidebandAntitagQcd=binsToList(SidebandAntitagQCD)
	contributionsPerBin=[]
	for i in range(len(tagsForSignalRegion)):
                tmpcontributions = [];
                tmpcontributions.append('sig');
                tmpcontributions.append('WJets');
                tmpcontributions.append('TTbar');
                tmpcontributions.append('ZJets');
                tmpcontributions.append('QCD');
                contributionsPerBin.append( tmpcontributions)
        SideBandAntitagRegion = searchRegion('sidebandantiag', contributionsPerBin, tagsForSignalRegion)	
	SideBandAntitagRegion_Rates = [];
        SideBandAntitagRegion_Obs = [];
	for i in range(SideBandAntitagRegion._nBins):
		tmpList=[]
                tmpList.append(SidebandAntitagSignalCont[i])#include contamination in control bins!
                tmpList.append(SidebandAntitagW[i])
                tmpList.append(SidebandAntitagTT[i])
                tmpList.append(SidebandAntitagZ[i])
                tmpList.append(SidebandAntitagQcd[i])
		sidebandobs=SidebandAntitagW[i]+SidebandAntitagTT[i]+SidebandAntitagZ[i]+SidebandAntitagQcd[i]
		SideBandAntitagRegion_Rates.append(tmpList);
		SideBandAntitagRegion_Obs.append(sidebandobs)
	SideBandAntitagRegion.fillRates(signalRegion_Rates);
	SideBandAntitagRegion.writeRates()
        SideBandAntitagRegion.setObservedManually(SideBandAntitagRegion_Obs);

	#Do ABCD A=B*C/D
	
	#signalRegion Nuisances:
	for i in range(len(tagsForSignalRegion)):
		print "SR %g AT %g SB %g SBAT %g " %(SRTT[i],AntitagTT[i], SidebandTT[i], SidebandAntitagTT[i]) 
		signalRegion.addSingleSystematic("QcdBkg_AntiTag"+str(i), 'lnU', ['QCD'], 100, '', i)
		signalRegion.addSingleSystematic("QcdBkg_Sideband"+str(i), 'lnU', ['QCD'], 100, '', i)	
		signalRegion.addSingleSystematic("ZBkg_AntiTag"+str(i), 'lnU', ['ZJets'], 100, '', i)
		signalRegion.addSingleSystematic("ZBkg_Sideband"+str(i), 'lnU', ['ZJets'], 100, '', i)	
		signalRegion.addSingleSystematic("WBkg_AntiTag"+str(i), 'lnU', ['WJets'], 100, '', i)
		signalRegion.addSingleSystematic("WBkg_Sideband"+str(i), 'lnU', ['WJets'], 100, '', i)	
		signalRegion.addSingleSystematic("TTBkg_AntiTag"+str(i), 'lnU', ['TTbar'], 100, '', i)
		signalRegion.addSingleSystematic("TTBkg_Sideband"+str(i), 'lnU', ['TTbar'], 100, '', i)	
		#B to SR
		AntiTagRegion.addSingleSystematic("QcdBkg_AntiTag"+str(i), 'lnU', ['QCD'], 100, '', i)
		AntiTagRegion.addSingleSystematic("ZBkg_AntiTag"+str(i), 'lnU', ['ZJets'], 100, '', i)
		AntiTagRegion.addSingleSystematic("WBkg_AntiTag"+str(i), 'lnU', ['WJets'], 100, '', i)
		AntiTagRegion.addSingleSystematic("TTBkg_AntiTag"+str(i), 'lnU', ['TTbar'], 100, '', i)
		#C/D to SR
		SideBandRegion.addSingleSystematic("TTBkg_Sideband"+str(i), 'lnU', ['TTbar'], 100, '', i)	
		SideBandRegion.addSingleSystematic("QcdBkg_Sideband"+str(i), 'lnU', ['QCD'], 100, '', i)	
		SideBandRegion.addSingleSystematic("WBkg_Sideband"+str(i), 'lnU', ['WJets'], 100, '', i)	
		SideBandRegion.addSingleSystematic("ZBkg_Sideband"+str(i), 'lnU', ['ZJets'], 100, '', i)	
		
		#ratio for C/D for SB region
		SideBandRegion.addSingleSystematic("TTBkg_SidebandAntitag"+str(i), 'lnU', ['TTbar'], 100, '', i)	
		SideBandRegion.addSingleSystematic("QcdBkg_SidebandAntitag"+str(i), 'lnU', ['QCD'], 100, '', i)	
		SideBandRegion.addSingleSystematic("WBkg_SidebandAntitag"+str(i), 'lnU', ['WJets'], 100, '', i)	
		SideBandRegion.addSingleSystematic("ZBkg_SidebandAntitag"+str(i), 'lnU', ['ZJets'], 100, '', i)	

		SideBandAntitagRegion.addSingleSystematic("TTBkg_SidebandAntitag"+str(i), 'lnU', ['TTbar'], 100, '', i)	
		SideBandAntitagRegion.addSingleSystematic("QcdBkg_SidebandAntitag"+str(i), 'lnU', ['QCD'], 100, '', i)	
		SideBandAntitagRegion.addSingleSystematic("WBkg_SidebandAntitag"+str(i), 'lnU', ['WJets'], 100, '', i)	
		SideBandAntitagRegion.addSingleSystematic("ZBkg_SidebandAntitag"+str(i), 'lnU', ['ZJets'], 100, '', i)	
	signalRegion.writeCards( odir );
	AntiTagRegion.writeCards(odir);
	SideBandRegion.writeCards(odir);
	SideBandAntitagRegion.writeCards(odir);
			
	#print odir
