import sys
from singleBin import *

class searchRegion:

	def __init__( self ,name, binLabels, refhisto ) :

		self._regionName = name;
		self._binLabels = binLabels;
		self._refhisto = refhisto;

		self._nBins = self._refhisto.GetNbinsX();
		self._singleBins = [];
		for i in range(self._nBins):
			self._singleBins.append( singleBin(self._regionName + str(i), self._refhisto.GetXaxis().GetBinLabel(i+1), self._binLabels, i ) );

		print "nbins = ", self._nBins;

	def fillRates(self, histograms):

		if len(histograms) != len(self._binLabels): 
			raise Exception("There is a mismatch in histogram input")

		for i in range(self._nBins):
			tmprates = [];
			for j in range(len(histograms)):
				tmprates.append( histograms[j].GetBinContent(i+1))
			self._singleBins[i].setRates( tmprates );
			self._singleBins[i].writeRates();
		
	def addSingleSystematic(self,sysname,systype,channel,val,identifier='',index=None):
		
		for i in range(self._nBins): 
			if identifier in self._singleBins[i]._tag:
				if index == None or index == self._singleBins[i]._index:
					# print identifier, " in ", self._singleBins[i]._tag;
					self._singleBins[i].addSystematic( sysname, systype, channel, val );

	def addSystematicByBinTag(self):
		print "this does nothing at the moment"

	def writeCards(self, odir):
		for i in range(self._nBins):
			self._singleBins[i].writeCard( odir ); 

	def GetNbins(self):
		return self._nBins;