import sys

class singleBin:

	def __init__( self , name, tag, binLabels, index ):

		self._name = name;
		self._tag  = tag;
		self._index  = index;
		self._binLabels = binLabels;
		self._rates = [];
		self._allLines = [];

		#print "bin tag = ", tag, index

	def setRates( self, rates ):

		self._rates = rates;

	def writeRates( self ):

		#############################
		# yield part of the datacard
		line = "#the tag = %s \n" % (self._tag);
		self._allLines.append(line);
		
		line = "imax 1 #number of channels \n";
		self._allLines.append(line);
		line = "jmax %i #number of backgrounds \n" % (len(self._binLabels)-1);
		self._allLines.append(line);
		self._allLines.append("kmax * nuissance \n");
		self._allLines.append("------------ \n");

		line = "bin Bin"+self._name+"\n";
		self._allLines.append(line);
		
		line = "observation "+str(sum(self._rates))+"\n";
		self._allLines.append(line);

		line = "bin ";
		for i in range(len(self._binLabels)): line += "Bin"+self._name + " ";
		line += "\n";
		self._allLines.append(line);

		line = "process ";
		for i in range(len(self._binLabels)): line += self._binLabels[i] + " ";
		line += "\n";
		self._allLines.append(line);

		line = "process ";
		for i in range(len(self._binLabels)): line += str(i) + " ";
		line += "\n";
		self._allLines.append(line);

		line = "rate ";
		zeroProxy = 0.0001;
		for rate in self._rates: 
			if rate < 0.000001: line += str(zeroProxy) + " ";
			else: line += "%.5f " % (rate);
		line += "\n";
		self._allLines.append(line);

		self._allLines.append("------------ \n");

	def addSystematic(self,sysname,systype,bins,val):

		line = "";
		line += sysname + " " + systype + " ";
		for i in range(len(self._binLabels)): 
			if self._binLabels[i] in bins: 
				if self._rates[i] < 0.000001 and systype == 'lnU': line += str(val*1000) + " ";
				else: line += str(val) + " ";
			else: line += "- ";
		line += "\n";
		self._allLines.append(line);

	def writeCard( self, odir ):
		
		ofile = open(odir+'/card_'+self._name+'.txt','w');
		for line in self._allLines: ofile.write(line);
		ofile.close();
