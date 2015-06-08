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

	#signals = ['SMSqqqq1000','SMSqqqq1400','SMStttt1200','SMStttt1500']
	signals = ['SMSqqqq1000']
	
	for sig in signals:
		
		# tag = 'SinglePhoton1'
		# command = 'python buildCards-ZvvOnly-SinglePhoton1.py -b --signal %s --tag %s' % (sig,tag); os.system(command);
		# command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);

		tag = 'DrellYan2'
		command = 'python buildCards-ZvvOnly-Zll2.py -b --signal %s --tag %s' % (sig,tag); os.system(command);
		command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);
		
		# tag = 'LowDPhi1'
		# command = 'python buildCards-QCDOnly-LowDPhi1.py -b --signal %s --tag %s' % (sig,tag); os.system(command);
		# command = 'python combineAllCards.py -b --run --dir testCards-%s-%s' % (tag,sig); os.system(command);

