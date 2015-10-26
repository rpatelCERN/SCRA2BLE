from ROOT import *
import os
import math
import sys
from array import array
from searchRegion import *
from singleBin import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option("--signal", dest="signal", default = 'SMSqqqq',help="mass of LSP", metavar="signal")
parser.add_option("--tag", dest="tag", default = 'SinglePhoton1',help="mass of LSP", metavar="tag")
parser.add_option("--mGo", dest="mGo", default='1000', help="Mass of Gluino", metavar="mGo")
parser.add_option("--mLSP", dest="mLSP", default='900', help="Mass of LSP", metavar="mLSP")
(options, args) = parser.parse_args()


#########################################################################################################
def getFittedMu(fn):
	
	output = [];

	tf = TFile(fn);
	tt = tf.Get("limit")
	tt.GetEntry(0);
	output.append( tt.limit );
	tt.GetEntry(1);
	output.append( tt.limit );
	tt.GetEntry(2);
	output.append( tt.limit );

	print output
	return output

def getLimit(fn):

	tf = TFile(fn);
	tt = tf.Get("limit")
	tt.GetEntry(2);
	output = tt.limit;

	return output

def getSignif(fn):
	
	tf = TFile(fn);
	tt = tf.Get("limit")
	tt.GetEntry(0);

	print "[getSignif], ", tt.limit
	return tt.limit;

#########################################################################################################
if __name__ == '__main__':
	
	#signals = ['SMSqqqq1400','SMSqqqq1000']
	#signals = ['SMSqqqq1400']
	#signals = ['SMSbbbb1500','SMSbbbb1000','SMStttt1500','SMStttt1200']	
	signalmodel=options.signal+options.mGo
	signals = [signalmodel]
	#mus = [0.0,0.5,1.0 ,1.5, 2.0, 2.5, 3.0,3.5, 4.0,4.5, 5.0];
	#mus = [10000.0];
	mus=[1.0]
	#lumis = [3.0,10.0];
	lumis = [1.3];

	#variations = ['qcdOnly','zvvOnly','llpOnly','tauOnly']
	#variations = ['allNotau','llpOnly', 'tauOnly']
	# variations = ['allBkgs','allNoqcd','allNozvv','allNollp','allNotau']
	#variations=['allNoqcd','allNozvv','allNollp','allNotau']
	#variations = ['qcdOnly' ]
	variations = ['allBkgs']
	#variations=['allNozvv']
	# variations=['onlyLep']
	#variations=['tauOnly']
	#variations=['allBkgs']

	job_postfix = "%s_%s_%s" % (options.signal,options.mGo,options.mLSP);
	fout = TFile("results_%s.root" % (job_postfix), "RECREATE");
	tout = TTree("results","results");   
	# identifier    = array( 'c', [ 'c' ] );  
	identifier = std.string()
	limit        = array( 'f', [ 0. ] );  
	significance = array( 'f', [ 0. ] );  
	fittedMu     = array( 'f', [ 0. ] );
	tout.Branch('identifier',identifier);
	tout.Branch("limit",limit,"limit/F");
	tout.Branch("significance",significance,"significance/F");
	tout.Branch("fittedMu",fittedMu,"fittedMu/F");

	for lumi in lumis: 
		print "=========>>> LUMI is ", lumi
		for sig in signals:
			for mu in mus:
				for vary in variations: 
					tag = vary;
					combOpt = '';
					if vary == 'allBkgs':  combOpt = '--allBkgs'
					if vary == 'qcdOnly':  combOpt = '--qcdOnly'
					if vary == 'zvvOnly':  combOpt = '--zvvOnly'
					if vary == 'llpOnly':  combOpt = '--llpOnly'
					if vary == 'tauOnly':  combOpt = '--tauOnly'
					if vary == 'allNoqcd': combOpt = '--tauOnly --zvvOnly --llpOnly'
					if vary == 'allNozvv': combOpt = '--tauOnly --qcdOnly --llpOnly'
					if vary == 'allNollp': combOpt = '--tauOnly --zvvOnly --qcdOnly'
					if vary == 'allNotau': combOpt = '--qcdOnly --zvvOnly --llpOnly'
					if vary == 'allNolep': combOpt = '--qcdOnly --zvvOnly'
					if vary == 'onlyLep':  combOpt = '--tauOnly --llpOnly'

					command = 'python buildCards-AllBkgsMassScanNew.py -b %s --signal  %s --tag %s --lumi %0.1f --mu %0.1f --mGo=%s --mLSP=%s' % (combOpt,options.signal,tag,lumi,mu, options.mGo, options.mLSP); os.system(command);
					
					the_odir = 'testCards-%s-%s_%s_%s-%1.1f-mu%0.1f' % (tag,options.signal,options.mGo, options.mLSP, lumi,mu);
					allcardnames = os.listdir(the_odir);
					command = 'combineCards.py ';
					for cn in allcardnames:
						if 'card_' in cn: command += " " + the_odir+'/'+cn;
					command += " > "+the_odir+'/allcards.txt'
					os.system(command);
					combine_cmmd = "text2workspace.py %s/allcards.txt -o %s/allcards.root" % (the_odir,the_odir);
					os.system(combine_cmmd);
					
					# run significance
					combine_cmmd = "combine -M ProfileLikelihood --signif %s/allcards.root -n %s" % (the_odir,the_odir); os.system(combine_cmmd);
					# run max likelihood fit
					combine_cmmd = "combine -M MaxLikelihoodFit %s/allcards.root -n %s " % (the_odir,the_odir); 
					os.system(combine_cmmd);
					# run asymptotic
					combine_cmmd = "combine -M Asymptotic %s/allcards.root -n %s" % (the_odir,the_odir); os.system(combine_cmmd);

					dicttag = "%s_%s_%.1f" % (tag,sig,lumi);

					identifier = dicttag;
					fittedMu[0] = getFittedMu( "higgsCombinetestCards-%s-%s_%s_%s-%0.1f-mu%0.1f.MaxLikelihoodFit.mH120.root" % (tag,options.signal, options.mGo, options.mLSP,lumi,mu) )[0];
                                        significance[0]=getSignif( "higgsCombinetestCards-%s-%s_%s_%s-%0.1f-mu%0.1f.ProfileLikelihood.mH120.root" % (tag,options.signal, options.mGo, options.mLSP,lumi,mu) ) ;
                                        limit[0] = getLimit( "higgsCombinetestCards-%s-%s_%s_%s-%0.1f-mu%0.1f.Asymptotic.mH120.root" % (tag,options.signal, options.mGo, options.mLSP,lumi,mu) ) ;
					#significance[0] = -99.;
					#limit[0] = -99.;
					tout.Fill();
	fout.cd();
	tout.Write();
	fout.Close();







