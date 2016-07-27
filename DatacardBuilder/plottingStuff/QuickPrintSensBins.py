from ROOT import *
#import ROOT
import sys
import operator
def ExtractFile(iname):
	f = TFile(iname);
	t = f.Get("limit");
	Lim=[]
	dictBinsLim={}
	dictBinsObsLim={}
	OneOverLSquared=0;

	for event in t:
		if event.quantileExpected < 0.51 and event.quantileExpected>0.49: #continue
			dictBinsLim[int(event.mh)]=event.limit
			ExpUL=event.limit
			OneOverLSquared=OneOverLSquared+1.0/(ExpUL*ExpUL)
		if event.quantileExpected < 0:
			dictBinsObsLim[int(event.mh)]=event.limit
	sortedLimbins=sorted(dictBinsLim.items(), key=operator.itemgetter(1))
	bins=[]
	ObsLim=[]
	SensBinsOneOverL=0
	for ibin in sortedLimbins:
		ExpUL=ibin[1]
		Lim.append(ExpUL)
		bins.append(int(ibin[0]))	
		SensBinsOneOverL=SensBinsOneOverL+(1.0/(ExpUL*ExpUL))
		if SensBinsOneOverL/OneOverLSquared>0.7:break
	#t.GetEntry(5);
	#Lim.append(t.limit)
	return Lim,bins
def ExtractObsFile(iname,searchbins):
	f = TFile(iname);
	t = f.Get("limit");
	ObsLim=[]
	for s in searchbins:
		for event in t:
			if event.quantileExpected>0:continue
			if  s==int(event.mh):
				ObsLim.append(event.limit)
	#t.GetEntry(5);
	#Lim.append(t.limit)
	return ObsLim

if __name__ == '__main__':
	models=["T1tttt", "T1tttt", "T1bbbb", "T1bbbb", "T1qqqq", "T1qqqq", "T2bb", "T2bb", "T5qqqqVV","T5qqqqVV", "T2tt", "T2tt"]
	Mgos=[1200,1700,1200,1800,1100,1750,600,800,1300,1700,500,850]
	MLsp=[800,400,1000,600,900,200,400,100,900,200,300,100]	
	#models=["SMSbbbb1500","SMSbbbb1000","SMStttt1500","SMStttt1200","SMSqqqq1400","SMSqqqq1000","SMStt850", "SMStt500","SMStt425" ]
	#printModels=["T1bbbb(1500, 100)", "T1bbbb(1000, 800)", "T1tttt(1500, 100)", "T1tttt(1200, 800)", " T1qqqq(1400, 100)",  "T1qqqq(1000, 900)", "T2tt(850,100)", "T2tt(500,325)","T2tt(425,325)"]
	fsig=TFile("inputHistograms/FullSim/RA2bin_signal.root", "READ")
	
	HistoLabels=fsig.Get("RA2bin_SMStttt1200")
	mode="allBkgs"
	PrefitErrorUp=[]
        PrefitErrorDn=[]
	fprefit=open("plottingStuff/ParsedInputPrefit.txt", 'r')
	for line in fprefit:
		parse=line.split(" ")
		PrefitErrorUp.append(float(parse[2]))
		PrefitErrorDn.append(float(parse[3]))
	Pulls=[]
	
	for m in range(len(models)):
		idir="./testCards-allBkgs-%s_%d_%d-7.7-mu0.0/" %(models[m], Mgos[m], MLsp[m])
		YieldsFile=TFile(idir+"/yields.root", "READ")
		histqcd=YieldsFile.Get("QCD")
	        histZ=YieldsFile.Get("Zvv")
                histTau=YieldsFile.Get("tau")
                histLL=YieldsFile.Get("LL")
		signalFile=TFile("./inputHistograms/fastsimSignal%s/RA2bin_signal.root" %models[m], "READ")
		signal=signalFile.Get("RA2bin_%s_%d_%d_fast" %(models[m],Mgos[m], MLsp[m]))
		signal.Scale(7700)
		hsprefit = THStack();
		hsprefit.Add(histZ);
		hsprefit.Add(histqcd);
		hsprefit.Add(histLL);
		hsprefit.Add(histTau);
		hsprefit_tot = hsprefit.GetStack().Last();		
		DataHist=YieldsFile.Get("data")
		ExpUL=ExtractFile(idir+"%s%d_%d.root" %(models[m], Mgos[m], MLsp[m]))[0]
		searchbins=ExtractFile(idir+"%s%d_%d.root" %(models[m], Mgos[m], MLsp[m]))[1]
		ObsUL=ExtractObsFile(idir+"%s%d_%d.root" %(models[m],Mgos[m], MLsp[m]), searchbins)
		for i in range(len(searchbins)):
			s=signal.GetBinContent(searchbins[i]+1)
			sAcc=s/signal.Integral()
        	        b=hsprefit_tot.GetBinContent(searchbins[i]+1)
			q=2*(sqrt(s+b)-sqrt(b))
			Obs=DataHist.GetBinContent(searchbins[i]+1)
			Pull=DataHist.GetBinContent(searchbins[i]+1)-b
			
			if Pull>=0:
				if DataHist.GetBinContent(i)>0.0:
                         		Pull=Pull/sqrt(Obs+(PrefitErrorUp[searchbins[i]]*PrefitErrorUp[searchbins[i]]))
				else: Pull=Pull/sqrt(1+(PrefitErrorUp[searchbins[i]]*PrefitErrorUp[searchbins[i]])) 
			else:
				if DataHist.GetBinContent(i)>0.0:
                                	Pull=Pull/sqrt(Obs+(PrefitErrorDn[searchbins[i]]*PrefitErrorDn[searchbins[i]]))
			 	else:
					Pull=Pull/sqrt(1.0+(PrefitErrorDn[searchbins[i]]*PrefitErrorDn[searchbins[i]]))		
			label=HistoLabels.GetXaxis().GetBinLabel(searchbins[i]+1)
			print "%s$(%d,%d)$ & %s & %2.3f & %2.3f & %2.2f & %2.2f & %d & %g & %1.2f & %1.2f \\\\" %(models[m], Mgos[m], MLsp[m],label,s,sAcc,q,b,Obs,Pull,ExpUL[i],ObsUL[i])
			#print ExpUL, ObsUL, searchbins

		#print "%s(%d,%d) & %1.2f & %1.2f \\\\" %(models[m], Mgos[m], MLsp[m],ExpUL,ObsUL)
