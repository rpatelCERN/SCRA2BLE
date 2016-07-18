from ROOT import *
import numpy as np
import mmap
import time
import sys
import operator
#flist=open("listofFiles%s.txt" %sys.argv[1], 'r')
#with open('LatestXsecGluGlu.txt', 'r') as input:
signalFile=TFile("../inputHistograms/fastsimSignal%s/RA2bin_signal.root" %sys.argv[1], "READ")

mGo=[]
mLsp=[]
names = [k.GetName() for k in signalFile.GetListOfKeys()]
for n in names:
        parse=n.split('_')
        #if parse[1]=="T1bbbb":
        #models.append(parse[1])
        mGo.append(int(parse[2]))
	mLsp.append(int(parse[3]))
#for line in flist:
#        fname=line.split('_')
#        mGo.append(float(fname[2]))
#        end=fname[3].split('.')
#        mLsp.append(float(end[0]))
PrefitErrorUp=[]
PrefitErrorDn=[]
fprefit=open("ParsedInputPrefit.txt", 'r')
for line in fprefit:
	parse=line.split(" ")
        PrefitErrorUp.append(float(parse[2]))
        PrefitErrorDn.append(float(parse[3]))
	print parse
QScan=TGraph2D()
QScan.SetName("QScan")
WSigma=TGraph2D()
WSigma.SetName("WSigma")
#theDir='testCards-allBkgs-SMSt-7.6-mu0.0/'
theDir='../testCards-allBkgs-T1bbbb_1200_800-7.6-mu0.0/' 
#theDir='./testCards-allBkgs-T2tt_%d_%d-2.6-mu0.0/' %(600, 300)
YieldsFile=TFile(theDir+"/yields.root", "READ")
histqcd=YieldsFile.Get("QCD")
histZ=YieldsFile.Get("Zvv")
histTau=YieldsFile.Get("tau")
histLL=YieldsFile.Get("LL")
hsprefit = THStack();
hsprefit.Add(histZ);
hsprefit.Add(histqcd);
hsprefit.Add(histLL);
hsprefit.Add(histTau);
hsprefit_tot = hsprefit.GetStack().Last();
DataHist=YieldsFile.Get("data")
for m in range(len(mGo)):
	#print mGo[m], mLsp[m]
	signal=signalFile.Get("RA2bin_%s_%d_%d_fast" %(sys.argv[1],int(mGo[m]), int(mLsp[m])))
	signal.Scale(7600)
	QHighSTotal=0
	PullWeighted=0
        dictQ={}
	Totalq2=0
        for i in range(1,161):
                s=signal.GetBinContent(i)
                b=hsprefit_tot.GetBinContent(i)
                q=2*(sqrt(s+b)-sqrt(b))
                Totalq2=Totalq2+(q*q)
                dictQ[i]=q*q
        sortedQbins=sorted(dictQ.items(), key=operator.itemgetter(1))
        sortedQbins.reverse()
        #print sortedQbins
        for i in range(1,161):
                s=signal.GetBinContent(i)
                b=hsprefit_tot.GetBinContent(i)
                q=2*(sqrt(s+b)-sqrt(b))
                binlabel=signal.GetXaxis().GetBinLabel(i)
        fractionalQ=0
        cutoff=1.0
        for ibin in sortedQbins:
                fractionalQ=fractionalQ+(ibin[1]*ibin[1])
                #if fractionalQ/Totalq2>cutoff:break	
		i=ibin[0]
		s=signal.GetBinContent(i)
		b=hsprefit_tot.GetBinContent(i)
		Q=2*(sqrt(s+b)-sqrt(b))
		if(Q>0.0):
			QHighSTotal=QHighSTotal+(Q*Q)
  			Pull=DataHist.GetBinContent(i)-hsprefit_tot.GetBinContent(i)
                	#if DataHist.GetBinContent(i)>0.0:
			if Pull>0:
                        	if DataHist.GetBinContent(i)>0.0:
					Pull=Pull/sqrt(DataHist.GetBinContent(i)+(PrefitErrorUp[i-1]*PrefitErrorUp[i-1]))
				else:
                                        Pull=Pull/sqrt(1.0+(PrefitErrorUp[i-1]*PrefitErrorUp[i-1]))
			else:
				if DataHist.GetBinContent(i)>0.0:Pull=Pull/sqrt(DataHist.GetBinContent(i)+(PrefitErrorDn[i-1]*PrefitErrorDn[i-1]))
				else: Pull=Pull/sqrt(1.0+(PrefitErrorDn[i-1]*PrefitErrorDn[i-1]))
					
			PullWeighted=PullWeighted+(Pull*Q*Q)
			#if mGo[m]==600 and mLsp[m]==300:print Pull

	if QHighSTotal>0:
		#if mGo[m]==600 and mLsp[m]==300:
		print PullWeighted/QHighSTotal
		WSigma.SetPoint(WSigma.GetN(), mGo[m], mLsp[m],PullWeighted/QHighSTotal)
	else:
		WSigma.SetPoint(WSigma.GetN(), mGo[m], mLsp[m],0.0)
        QScan.SetPoint(QScan.GetN(), mGo[m], mLsp[m], sqrt(QHighSTotal))

QScan.SetName("QScan")
QScan.SetNpx(128)
QScan.SetNpy(160)
WSigma.SetName("WSigma")
WSigma.SetNpx(128)
WSigma.SetNpy(160)
hWsig=WSigma.GetHistogram()
hQ=QScan.GetHistogram()
c=TCanvas("c","",800,800);
QScan.Draw("colz")
QLim=TGraph()
QLim.SetName("QLim")
QLim= QScan.GetContourList(2.);
fileOut=TFile("QScan%s.root" %sys.argv[1], "RECREATE")
QLim.Write("QLim")
hQ.Write("QScan")
hWsig.Write("hWsig")
#fileOut.Write()
#c.Print("test.pdf")
fileOut.Close()
#if hlim is None: print "NONE"
#time.sleep(60)
