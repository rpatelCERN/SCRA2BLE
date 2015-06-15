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

def getSignif(fn):
	
	tf = TFile(fn);
	tt = tf.Get("limit")
	tt.GetEntry(0);

	print "[getSignif], ", tt.limit
	return tt.limit;

#########################################################################################################
if __name__ == '__main__':

	#signals = ['SMSqqqq1000','SMSqqqq1400','SMStttt1200','SMStttt1500','SMSbbbb1000','SMSbbbb1500']
	# signals = ['SMSqqqq1000','SMSbbbb1000']
	signals = ['SMSqqqq1000']
	
<<<<<<< HEAD
	# mus = [0.5,1.0,1.5,2.0];
	mus = [0.5];

	lumis = [3.0,10.0];

	fittedMus = {};
	injectedMus = {};
	significances = {};

	for lumi in lumis: 
		for sig in signals:
			for mu in mus:
	
				dicttag = "%s_%.1f" % (sig,lumi);

				tag = 'AllButQCD';
				command = 'python buildCards-AllButQCD.py -b --signal  %s --tag %s --lumi %0.1f --mu %0.1f' % (sig,tag,lumi,mu); os.system(command);
				command = 'python combineAllCards.py -b --run --dir testCards-%s-%s-%0.1f-mu%0.1f' % (tag,sig,lumi,mu); os.system(command);
=======
	for sig in signals:
		
		# tag = 'SinglePhoton1'
		# command = 'python buildCards-ZvvOnly-SinglePhoton1.py -b --signal %s --tag %s' % (sig,tag); os.system(command);
		# command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);

		# tag = 'DrellYan2'
		# command = 'python buildCards-ZvvOnly-Zll2.py -b --signal %s --tag %s' % (sig,tag); os.system(command);
		# command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);

		# tag = 'Hybrid3'
		# command = 'python buildCards-ZvvOnly-Hybrid3.py -b --signal %s --tag %s' % (sig,tag); os.system(command);
		# command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);
		
		# tag = 'LowDPhi1'
		# command = 'python buildCards-QCDOnly-LowDPhi1.py -b --signal %s --tag %s' % (sig,tag); os.system(command);
		# command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);

		tag = 'LowDPhi2'
                command = 'python buildCards-QCDOnly-LowDPhiProxy.py -b --signal %s --tag %s' % (sig,tag); os.system(command);
                command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);
		
		# tag = 'HadTau';
		# command = 'python buildCards-HadTauOnly-tautempl.py -b --signal %s --tag %s' % (sig,tag); os.system(command);
		# command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);

		# tag = 'LL';
		# command = 'python buildCards-SLOnly-classic.py -b --signal  %s --tag %s' % (sig,tag); os.system(command);
		# command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);

	#	tag = 'AllButQCD';
	#	command = 'python buildCards-AllButQCD.py -b --signal  %s --tag %s' % (sig,tag); os.system(command);
	#	command = 'python combineAllCards.py -b --run --dir testCards-%s-%s ' % (tag,sig); os.system(command);
>>>>>>> 454b982a79aca1542bfc00bbe5ec3bd17fcc161f

				significances[dicttag] = getSignif( "higgsCombinetestCards-AllButQCD-SMSqqqq1000-%0.1f-mu%0.1f.ProfileLikelihood.mH120.root" % (lumi,mu) )
				fittedMus[dicttag] = getFittedMu( "higgsCombinetestCards-AllButQCD-SMSqqqq1000-%0.1f-mu%0.1f.MaxLikelihoodFit.mH120.root" % (lumi,mu) )
				injectedMus[dicttag] = mu;

