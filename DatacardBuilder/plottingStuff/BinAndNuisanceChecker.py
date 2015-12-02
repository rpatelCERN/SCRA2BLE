import ROOT as root
from ROOT import *
import ROOT
import time
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import math
import tdrstyle
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPadLeftMargin(0.12);
ROOT.gStyle.SetPadRightMargin(0.08);
ROOT.gStyle.SetPadTopMargin(0.08);
ROOT.gStyle.SetPalette(1);


#########################################################################################################
theDir = 'testCards-allBkgs-SMSbbbb1000-2.1-mu0.0'

def GetPrefitErrorsFromJack(fn):
        f = open(fn,'r');

        errup = [];
        errdn = [];
        for line in f:
                linelist = line.strip().split();
                # print linelist;
                errup.append( math.sqrt( float(linelist[4])*float(linelist[4]) + float(linelist[6])*float(linelist[6]) ) );
                errdn.append( math.sqrt( float(linelist[8])*float(linelist[8]) + float(linelist[10])*float(linelist[10]) ) );

        return (errup,errdn);

def getErrorFromCard(card,chan):

	lnSystematicsName = [];
	lnSystematicsVal = [];

	fcard=open(card)
	column = -1;
	sysLine = False;
	for line in fcard:
		parse=line.split(' ')
		if parse[0]=='process' and parse[1]=='sig':
			for i in range(len(parse)):
				if parse[i] == chan: 
					column = i;

		if "ln" in parse[1]: sysLine = True; #it's time to collect
		if sysLine and (parse[1] == "lnN" or parse[1] == "lnU"): 
			parse = [x for x in parse if x != '']				
			# print "blah,",parse[0],parse[column+1],column,parse				
			if parse[column+1] != "-": 
				# print "blah,",parse[0],parse[column+1],column
				lnSystematicsName.append( parse[0] );
				if '/' in parse[column+1]: 
					syssplit = parse[column+1].split('/');
					lnSystematicsVal.append(float(syssplit[1]));
				else:
					lnSystematicsVal.append(float(parse[column+1]));

	return (lnSystematicsName,lnSystematicsVal)

def getNuisanceNamesAndValuesZinv(c,tolerance):
	
	nameOfNuisances_Zinv = []
	valsOfNuisances_Zinv = []

	fcardname = "../"+theDir+"/card_signal%d.txt" %c;
	sphoton_index = c % 6 + 6*(c / 24);
	fcardname_Zinv = "../"+theDir+"/card_sphoton%d.txt" %sphoton_index;
	tmpname,tmpvals = getErrorFromCard(fcardname,"zvv");
	for i in range(len(tmpname)): 
		if math.fabs((float(tmpvals[i]) -1.)) > tolerance: 
			nameOfNuisances_Zinv.append( tmpname[i] );  valsOfNuisances_Zinv.append( tmpvals[i] );
	tmpname,tmpvals = getErrorFromCard(fcardname_Zinv,"zvv");
	for i in range(len(tmpname)): 
		if math.fabs((float(tmpvals[i]) -1.)) > tolerance and (not tmpname[i] in nameOfNuisances_Zinv): 
			nameOfNuisances_Zinv.append( tmpname[i] );  valsOfNuisances_Zinv.append( 1 + ( 1 - tmpvals[i] ) );

	return (nameOfNuisances_Zinv,valsOfNuisances_Zinv)

##########################################################################################
def getPrefitAndPostfitNuisance(nameOfNuisance):

	thePost = -99.;
	thePre = -99.;

	fin=TFile(".."+"/mlfit"+theDir+".root", "READ")
	fit_b  = fin.Get("fit_b")
	prefit = fin.Get("nuisances_prefit")

	fpf_b = fit_b.floatParsFinal()

	for i in range(fpf_b.getSize()):
		nuis_b = fpf_b.at(i)
		name   = nuis_b.GetName();
		nuis_b = fpf_b.find(name)
		nuis_p = prefit.find(name)
		if name == nameOfNuisance: 
			thePre = nuis_p.getVal();
			thePost = nuis_b.getVal();
			break;
	return (thePre,thePost)


##########################################################################################	

if __name__ == '__main__':
	
	fin=TFile(".."+"/mlfit"+theDir+".root", "READ")
	BinProcesses=fin.Get("norm_prefit");
	BinProcessesPostFit=fin.Get("norm_fit_b");
	fit_s  = fin.Get("fit_s")
	fit_b  = fin.Get("fit_b")
	prefit = fin.Get("nuisances_prefit")

	mybins=[]
	searchbins=[]
	hsprefit = THStack();
	hspostfit = THStack();

	for c in range(1,235):
		sig = BinProcesses.find("ch%d/sig" %c)
		Z   = BinProcesses.find("ch%d/zvv" %c)
		Q   = BinProcesses.find("ch%d/qcd" %c)
		T   = BinProcesses.find("ch%d/WTopHad" %c)
		L   = BinProcesses.find("ch%d/WTopSL" %c)
		
		if Q and Z:# only signal region bins have process QCD and Zinv 
			#print T.getVal(), L.getVal(),Z.getVal(), Q.getVal()
			mybins.append(c)
			#just need to find this once (mapping to search bins):
			for i in range(0,72):
				fcardname = "../"+theDir+"/card_signal%d.txt" %i;
				fcard=open(fcardname)
				fcard.seek(0)
				for line in fcard:
					parse=line.split(' ')
					if parse[0]=='rate':
						 eps=1e-4
						 if(abs(L.getVal()-float(parse[2]))<eps and abs(T.getVal()-float(parse[4]))<eps and abs(Z.getVal()-float(parse[6]))<eps and abs(Q.getVal()-float(parse[7]))<eps):
							searchbins.append(i)


	print "len(mybins) = ", len(mybins);
	errorsPrefitFromJack_Up,errorsPrefitFromJack_Dn  = GetPrefitErrorsFromJack("PreFitErrorsFromJack.txt");	
	for c in range(len(mybins)):
		if c > 5: break;

		print "++++++++++++"
		print "bin #",c

		Z   = BinProcesses.find("ch%d/zvv" %mybins[c])
		Q   = BinProcesses.find("ch%d/qcd" %mybins[c])
		T   = BinProcesses.find("ch%d/WTopHad" %mybins[c] )
		L   = BinProcesses.find("ch%d/WTopSL" % mybins[c])
		Zpos= BinProcessesPostFit.find("ch%d/zvv" %mybins[c])
		Qpos= BinProcessesPostFit.find("ch%d/qcd" %mybins[c])
		Tpos= BinProcessesPostFit.find("ch%d/WTopHad" %mybins[c])
		Lpos= BinProcessesPostFit.find("ch%d/WTopSL" %mybins[c])

		nameOfNuisances_Zinv,valsOfNuisances_Zinv = getNuisanceNamesAndValuesZinv(c, 0.05);

		# print nameOfNuisances_Zinv
		# print valsOfNuisances_Zinv	
		# print c, Z.getVal(), Zpos.getVal()
		
		print "prefit Zinv = ", round(Z.getVal(),5);	
		print "postfit Zinv = ", round(Zpos.getVal(),5);	
		print "nuisances with uncertainty above 5%";
		total = 0.;
		for i in range(len(nameOfNuisances_Zinv)):
			if valsOfNuisances_Zinv[i] < 100:
				print nameOfNuisances_Zinv[i],", value in card: ",round(float(valsOfNuisances_Zinv[i]),4)
				preNuis,posNuis = getPrefitAndPostfitNuisance(nameOfNuisances_Zinv[i]);
				change = math.pow(float(valsOfNuisances_Zinv[i]),posNuis);
				print "    change (nevt) = ", round((change-1)*Z.getVal(),3)
				total += (change-1)*Z.getVal();
		print "total change = ", round(total,3)
		for i in range(len(nameOfNuisances_Zinv)):
			if valsOfNuisances_Zinv[i] >= 100:
				# print nameOfNuisances_Zinv[i],round(float(valsOfNuisances_Zinv[i]),4)
				preNuis,posNuis = getPrefitAndPostfitNuisance(nameOfNuisances_Zinv[i]);
				change = math.pow(float(valsOfNuisances_Zinv[i]),posNuis);
				print "*LNU* nuisance:",nameOfNuisances_Zinv[i],round(float(valsOfNuisances_Zinv[i]),4)," || change (nevt) = ", round((change-1)*Z.getVal(),3)
		print "++++++++++++"
	

	
