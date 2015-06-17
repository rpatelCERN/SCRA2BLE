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
	signals = ['SMSqqqq1000']
	#signals = ['SMSqqqq1000','SMSqqqq1400','SMStttt1200','SMStttt1500','SMSbbbb1000','SMSbbbb1500']
	# signals = ['SMSqqqq1000','SMSbbbb1000']
	# signals = ['SMSbbbb1500','SMSbbbb1000']
	
	#mus = [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0];
	mus = [1.0];

	# lumis = [3.0,10.0];
	lumis = [10.0];

	# variations = ['allBkgs','qcdOnly','zvvOnly','llpOnly','tauOnly']
	variations = ['allBkgs']

	identifiers = [];
	limits = [];
	fittedMus = [];
	injectedMus = [];
	significances = [];

	for lumi in lumis: 

		print "=========>>> LUMI is ", lumi

		for sig in signals:
			for mu in mus:
				for vary in variations: 
					tag = vary;
					command = 'python buildCards-AllBkgs.py -b --%s --signal  %s --tag %s --lumi %0.1f --mu %0.1f' % (vary,sig,tag,lumi,mu); os.system(command);
					command = 'python combineAllCards.py -b --run --dir testCards-%s-%s-%0.1f-mu%0.1f' % (tag,sig,lumi,mu); os.system(command);

					dicttag = "%s_%s_%.1f" % (tag,sig,lumi);
