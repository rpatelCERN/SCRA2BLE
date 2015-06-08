from ROOT import *

import math
import sys
import re

# clones bins 1-18 to other bins
def hutil_clone0BtoNB(h_in):

	translations = [
					['NJets1_BTags1',0.244],
					['NJets1_BTags2',0.047],
					['NJets1_BTags3',0.0045],
					['NJets2_BTags1',0.392],
					['NJets2_BTags2',0.132],
					['NJets2_BTags3',0.024],
					['NJets2_BTags1',0.50],
					['NJets2_BTags2',0.226],
					['NJets2_BTags3',0.057]
				   ]

	h_new = h_in.Clone();
	print "hutil_clone0BtoNB"

	for i in range(h_new.GetNbinsX()):
		binlabel = h_new.GetXaxis().GetBinLabel(i+1);
		
		ref_binlabel = None;
		for trans in translations: 
			if trans[0] in binlabel:
				ref_binlabel = re.sub("BTags.","BTags0",binlabel)
				newBinContent = getBinContentByLabel( h_in, ref_binlabel ) * trans[1];
				h_new.SetBinContent(i+1,newBinContent);

				# print binlabel,ref_binlabel;
				# print i, binlabel, ref_binlabel, h_in.GetBinContent(i+1) , " " , getBinContentByLabel( h_in, ref_binlabel ) ," ", newBinContent, " ", trans[1];

	return h_new;

##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

def getBinContentByLabel(h_in,label):

	binContent = -99;
	for i in range(h_in.GetNbinsX()):
		binlabel = h_in.GetXaxis().GetBinLabel(i+1);
		if binlabel == label: 
			binContent = h_in.GetBinContent(i+1);
			break;
	return binContent;




