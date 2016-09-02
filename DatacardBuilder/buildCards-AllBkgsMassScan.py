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

	sms = "SMS"+options.signal[2:]+options.mGo;
	if options.fastsim: sms = options.signal+'_'+options.mGo+'_'+options.mLSP;
	tag = options.tag;
	lumi = float(options.lumi);
	signalmu = float(options.mu);
	odir = 'testCards-%s-%s-%1.1f-mu%0.1f/' % ( tag,sms, lumi, signalmu );
	idir = 'inputHistograms/histograms_%1.1ffb/' % ( ((lumi)) );
	if os.path.exists(odir): os.system( "rm -rf %s" % (odir) );
	os.makedirs(odir);

	print odir, signalmu

	######################################################################
	######################################################################
	## 1. Get the input histograms from each of the background teams
	######################################################################
	######################################################################

	# --------------------------------------------
	# signal 
	signaldirtag = idir;
	if options.fastsim: 
		#signaldirtag += "/fastsimSignalScan";
	
		if "T2qq" in sms:  signaldirtag ="inputHistograms/fastsimSignalT2qq"
		if "T2tt" in sms:  signaldirtag ="inputHistograms/fastsimSignalT2tt"
		if "T2bb" in sms:  signaldirtag ="inputHistograms/fastsimSignalT2bb"
		if "T1tttt" in sms:  signaldirtag ="inputHistograms/fastsimSignalT1tttt"
		if "T1bbbb" in sms:  signaldirtag ="inputHistograms/fastsimSignalT1bbbb"
		if "T1qqqq" in sms:  signaldirtag ="inputHistograms/fastsimSignalT1qqqq"
		if "T5qqqqVV" in sms:  signaldirtag ="inputHistograms/fastsimSignalT5qqqqVV"
	signaltag = "RA2bin_"+sms;
	parse=sms.split('_')
	model=parse[0]
	#print parse
	signaltag+="_fast"                  
	signalSFB_file =TFile(signaldirtag+"/RA2Aggbin_signal.root");
	signalRegion_sigHist          = signalSFB_file.Get(signaltag);
	tagsForSignalRegion = binLabelsToList(signalRegion_sigHist);

	signalRegion_sigHist.Scale(lumi*1000);
	signalRegion_sigList = binsToList( signalRegion_sigHist );
	AggRegions_ObsList = textToList(idir+"/AggregateBinObs.txt",0);
	AggRegions_SLYieldsListStr = textToListStr(idir+"/AggregateBinYields.txt",0);
	AggRegions_TauYieldsListStr = textToListStr(idir+"/AggregateBinYields.txt",1);
	AggRegions_ZYieldsListStr = textToListStr(idir+"/AggregateBinYields.txt",2);
	AggRegions_QCDYieldsListStr = textToListStr(idir+"/AggregateBinYields.txt",3);
	#UNPACKING:
	SLYields=[]
	SLErrUp=[]
	SLErrDn=[]

	TauYields=[]
	TauErrUp=[]
	TauErrDn=[]

	ZYields=[]
	ZErrUp=[]
	ZErrDn=[]
	QCDYields=[]
	QCDErrUp=[]
	QCDErrDn=[]
	QValue=signalRegion_sigHist.Clone("QValue")
	for i in range(len(AggRegions_SLYieldsListStr)):
		SL=AggRegions_SLYieldsListStr[i].split(',')
		SLYields.append(float(SL[0]))
		SLErrUp.append(float(SL[1]))
		SLErrDn.append(float(SL[2]))

		Tau=AggRegions_TauYieldsListStr[i].split(',')
		TauYields.append(float(Tau[0]))
		TauErrUp.append(float(Tau[1]))
		TauErrDn.append(float(Tau[2]))

		Z=AggRegions_ZYieldsListStr[i].split(',')
		ZYields.append(float(Z[0]))
		ZErrUp.append(float(Z[1]))
		ZErrDn.append(float(Z[2]))

		QCD=AggRegions_QCDYieldsListStr[i].split(',')
		QCDYields.append(float(QCD[0]))
		QCDErrUp.append(float(QCD[1]))
		QCDErrDn.append(float(QCD[2]))
	for i in range(len(QCDYields)):
		S=signalRegion_sigList[i]
		B=SLYields[i]+TauYields[i]+ZYields[i]+QCDYields[i]
		Q=2*(sqrt(S+B)-sqrt(B))
		QValue.SetBinContent(i+1, Q*Q)
		print Q*Q,B,S
	AnalysisBin=QValue.GetMaximumBin()
	AlltagsForSignalRegion=["NJets3_BTags0_HT500_MHT500", "NJets3_BTags0_HT1500_MHT750","NJets5_BTags0_HT500_MHT500","NJets5_BTags0_HT1500_MHT750", "NJets9_BTags0_HT1500_MHT750", "NJets3_BTags2_HT500_MHT500","NJets3_BTags1_HT750_MHT750","NJets5_BTags3_HT500_MHT500","NJets5_BTags2_HT1500_MHT750","NJets9_BTags3_HT750_MHT750","NJets7_BTags1_HT300_MHT300","NJets5_BTags1_HT750_MHT750"]
	tagsForSignalRegion=[AlltagsForSignalRegion[AnalysisBin-1]]
	contributionsPerBin=[]
	#for i in range(len(signalRegion_sigList)):
	tmpcontributions = [];
	tmpcontributions.append('sig');
	tmpcontributions.append('SL');
	tmpcontributions.append('Tau');
	tmpcontributions.append('Z');
	tmpcontributions.append('QCD');
	contributionsPerBin.append(tmpcontributions)
	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)	
	tmpList=[]
	tmpList.append(signalRegion_sigList[AnalysisBin-1])
	if(SLYields[AnalysisBin-1]<0.001):tmpList.append(SLYields[AnalysisBin-1])
	else:tmpList.append(SLErrDn[AnalysisBin-1])
	if(TauYields[AnalysisBin-1]>0.001):tmpList.append(TauYields[AnalysisBin-1])
	else:tmpList.append(TauErrUp[AnalysisBin-1])
	if(ZYields[AnalysisBin-1]>0.001):tmpList.append(ZYields[AnalysisBin-1])
        else:tmpList.append(ZErrUp[AnalysisBin-1])
	if(QCDYields[AnalysisBin-1]>0.001):tmpList.append(QCDYields[AnalysisBin-1])
        else:tmpList.append(QCDErrUp[AnalysisBin-1])
	signalRegion_Rates = [];
	signalRegion_Rates.append(tmpList) #[signalRegion_sigList[AnalysisBin-1], SLYields[AnalysisBin],TauYields[AnalysisBin],ZYields[AnalysisBin],QCDYields[AnalysisBin]];
	signalRegion_Obs = [AggRegions_ObsList[AnalysisBin-1]];
	signalRegion.fillRates(signalRegion_Rates );
	signalRegion.setObservedManually(signalRegion_Obs)
	signalRegion.writeRates();
	if(1-SLErrDn[AnalysisBin-1]/SLYields[AnalysisBin-1]<0.0001):SLErrDn[AnalysisBin-1]=SLYields[AnalysisBin-1]-0.001
	if(1-TauErrDn[AnalysisBin-1]/TauYields[AnalysisBin-1]<0.0001):TauErrDn[AnalysisBin-1]=TauYields[AnalysisBin-1]-0.001
	if(1-ZErrDn[AnalysisBin-1]/ZYields[AnalysisBin-1]<0.0001):ZErrDn[AnalysisBin-1]=ZYields[AnalysisBin-1]-0.001
	if(1-QCDErrDn[AnalysisBin-1]/QCDYields[AnalysisBin-1]<0.0001):QCDErrDn[AnalysisBin-1]=QCDYields[AnalysisBin-1]-0.001
	if(SLYields[AnalysisBin-1]>0.001):signalRegion.addAsymSystematic('SLUnc','lnN', ['SL'], 1+SLErrUp[AnalysisBin-1]/SLYields[AnalysisBin-1], 1-SLErrDn[AnalysisBin-1]/SLYields[AnalysisBin-1], '', 0)
	else: signalRegion.addSingleGammaSystematic("SLUnc", 'gmN', ['SL'], 0, SLErrUp[AnalysisBin-1])
	if(TauYields[AnalysisBin-1]>0.001):signalRegion.addAsymSystematic('TauUnc','lnN', ['Tau'], 1+TauErrUp[AnalysisBin-1]/TauYields[AnalysisBin-1], 1-TauErrDn[AnalysisBin-1]/TauYields[AnalysisBin-1], '', 0)
	else:signalRegion.addSingleGammaSystematic("TauUnc", 'gmN', ['Tau'], 0, TauErrUp[AnalysisBin-1])
	if(ZYields[AnalysisBin-1]>0.001):signalRegion.addAsymSystematic('ZUnc','lnN', ['Z'], 1+ZErrUp[AnalysisBin-1]/ZYields[AnalysisBin-1], 1-ZErrDn[AnalysisBin-1]/ZYields[AnalysisBin-1], '', 0)
	else:signalRegion.addSingleGammaSystematic("ZUnc", 'gmN', ['Z'], 0, ZErrUp[AnalysisBin-1])
	if(QCDYields[AnalysisBin-1]>0.001):signalRegion.addAsymSystematic('QCDUnc','lnN', ['QCD'], 1+QCDErrUp[AnalysisBin-1]/QCDYields[AnalysisBin-1], 1-QCDErrDn[AnalysisBin-1]/QCDYields[AnalysisBin-1], '', 0)
	else:signalRegion.addSingleGammaSystematic("QCDUnc", 'gmN', ['QCD'], 0, QCDErrUp[AnalysisBin-1])
	signalRegion.writeCards( odir );
