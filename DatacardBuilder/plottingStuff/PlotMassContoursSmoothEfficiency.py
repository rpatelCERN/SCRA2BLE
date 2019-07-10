from ROOT import *
#import numpy as np
import mmap
import time
import sys
import os

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--model", dest="model", default = "T1tttt",help="SMS model", metavar="model")
(options, args) = parser.parse_args()
#flist=open("listofFiles%s.txt" %sys.argv[1], 'r')
#fgluxsec=open("LatestXsecGluGlu.txt", 'r')
dictXsec={}
dictXsecUnc={}
#with open('LatestXsecGluGlu.txt', 'r') as input:
#with open('LatestGluGluNNLO.txt', 'r') as input:
#with open('LatestSquarkNNLO.txt', 'r') as input:
with open('LatestSbottomStopNNLO.txt', 'r') as input:
        for line in input: #for ex. |225|2021.29|13.8804|
                elements = line.rstrip().split("|")
                dictXsec[int(elements[1])]=elements[2]
                dictXsecUnc[int(elements[1])]=elements[3]
                #print elements
mGo=[]
mLsp=[]
MissMgo=[]
MissMLsp=[]
limit=[]

#fileOut=TFile("MassScan%s.root" %sys.argv[1], "RECREATE")
fileOut=TFile("MassScan%s.root" %options.model, "RECREATE")
#names = next(os.walk("/eos/uscms/store/user/rgp230/SUSY/CheckYields/Run2ProductionV12/fastsimSignal%s/" %options.model))[2]
#names = next(os.walk("/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/"))[2]
names = next(os.walk("/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/"))[2]

for n in names:
	#print "nList ",n
	parse=n.split('_')
	if not "proc" in parse[1]:continue
	if not "MC2016" in parse[5]:continue
	if options.model==parse[2]:
		#print  parse
		mGo.append(float(parse[3]))
		mLsp.append(float(parse[4]))
		
		
SignifScan=TGraph2D()
SignifScan.SetName("SignifScan")

histoSignifScan=TH2D("histoSignifScan", "Signif. Scan (#sigma) ", 100, 0, 2500, 64,0,1600)
'''
MuScan=TGraph2D(len(mLsp))
MuScan.SetName("MuScan")
MuScanXsec=TGraph2D(len(mLsp))
MuScanXsec.SetName("MuScanXsec")
MuScanSup=TGraph2D(len(mLsp))
MuScanSup.SetName("MuScanSup")
MuScanSdn=TGraph2D(len(mLsp))
MuScanSdn.SetName("MuScanSdn")
MuScanObs=TGraph2D(len(mLsp))
MuScanObs.SetName("MuScanObs")
MuScanObsSup=TGraph2D(len(mLsp))
MuScanObsSup.SetName("MuScanObsSup")
MuScanObsSdn=TGraph2D(len(mLsp))
MuScanObsSdn.SetName("MuScanObsSdn")
'''
#idir = "/eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond/BugFix/forrishilpcT1tttt/";
idir = "/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/" #"/eos/uscms/store/user/arane/Limits_T1tttt/";
RunLumi=[ 35916.403 , 41521.425,21000.905,38196.951 ]
TotalLumi=RunLumi[0]+RunLumi[1]+RunLumi[2]+RunLumi[3];
for m in range(len(mGo)):
	if(int(mGo[m])==1625 and int(mLsp[m])>=1475):continue
	#if(int(mGo[m])==1625 and int(mLsp[m])==1500):continue
	#if(int(mGo[m])==1625 and int(mLsp[m])==1525):continue
	#if(int(mGo[m])==1625 and int(mLsp[m])==1550):continue
		#print "Check if this file is really empty before execution"
#		continue;
    	#if sys.argv[1]=="T1qqqq" and mGo[m]<400: continue
	filein1=TFile.Open(idir+"RA2bin_proc_%s_%s_%s_MC2016_fast.root" %(options.model,int(mGo[m]), int(mLsp[m])))
	filein2=TFile.Open(idir+"RA2bin_proc_%s_%s_%s_MC2017_fast.root" %(options.model,int(mGo[m]), int(mLsp[m])))
	filein3=TFile.Open(idir+"RA2bin_proc_%s_%s_%s_MC2018_fast.root" %(options.model,int(mGo[m]), int(mLsp[m])))
	filein4=TFile.Open(idir+"RA2bin_proc_%s_%s_%s_MC2018HEM_fast.root" %(options.model,int(mGo[m]), int(mLsp[m])))
	if dictXsec.get(mGo[m])==None:continue
	print mGo[m],dictXsec.get(mGo[m])
	
	t1 = filein1.Get("RA2bin_%s_%s_%s_MC2016_fast_nominalOrig"%(options.model,int(mGo[m]), int(mLsp[m])))
	t1.Scale(RunLumi[0])
	t2 = filein2.Get("RA2bin_%s_%s_%s_MC2017_fast_nominalOrig"%(options.model,int(mGo[m]), int(mLsp[m])))
	t2.Scale(RunLumi[1])
	t3 = filein3.Get("RA2bin_%s_%s_%s_MC2018_fast_nominalOrig"%(options.model,int(mGo[m]), int(mLsp[m])))
	t3.Scale(RunLumi[2])
	t4 = filein4.Get("RA2bin_%s_%s_%s_MC2018HEM_fast_nominalOrig"%(options.model,int(mGo[m]), int(mLsp[m])))
	t4.Scale(RunLumi[3])
	t1.Add(t2)
	t1.Add(t3)
	t1.Add(t4)
	t1.SetDirectory(0);
	g1 = filein1.Get("RA2bin_%s_%s_%s_MC2016_fast_genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
	g1.Scale(RunLumi[0])
	g2 = filein2.Get("RA2bin_%s_%s_%s_MC2017_fast_genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
	g2.Scale(RunLumi[1])
	g3 = filein3.Get("RA2bin_%s_%s_%s_MC2018_fast_genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
	g3.Scale(RunLumi[2])
	g4 = filein4.Get("RA2bin_%s_%s_%s_MC2018HEM_fast_genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
	g4.Scale(RunLumi[3])
	g1.Add(g2)
	g1.Add(g3)
	g1.Add(g4)
	if options.model=="T1tttt" or options.model=="T2tt" or options.model=="T5qqqqVV":
		e1 = filein1.Get("RA2bin_%s_%s_%s_MC2016_fast_SLe"%(options.model,int(mGo[m]), int(mLsp[m])))
		e1 = filein1.Get("RA2bin_%s_%s_%s_MC2016_fast_SLe"%(options.model,int(mGo[m]), int(mLsp[m])))
		e2 = filein2.Get("RA2bin_%s_%s_%s_MC2017_fast_SLe"%(options.model,int(mGo[m]), int(mLsp[m])))
		e3 = filein3.Get("RA2bin_%s_%s_%s_MC2018_fast_SLe"%(options.model,int(mGo[m]), int(mLsp[m])))
		e4 = filein4.Get("RA2bin_%s_%s_%s_MC2018HEM_fast_SLe"%(options.model,int(mGo[m]), int(mLsp[m])))
		m1 = filein1.Get("RA2bin_%s_%s_%s_MC2016_fast_SLm"%(options.model,int(mGo[m]), int(mLsp[m])))
		e1.Add(m1);
		m2 = filein2.Get("RA2bin_%s_%s_%s_MC2017_fast_SLm"%(options.model,int(mGo[m]), int(mLsp[m])))
		e2.Add(m2);
		m3 = filein3.Get("RA2bin_%s_%s_%s_MC2018_fast_SLm"%(options.model,int(mGo[m]), int(mLsp[m])))
		e3.Add(m3);
		m4 = filein4.Get("RA2bin_%s_%s_%s_MC2018HEM_fast_SLm"%(options.model,int(mGo[m]), int(mLsp[m])))
		e4.Add(m4);

		e1.Scale(RunLumi[0])
		e2.Scale(RunLumi[1])
		e3.Scale(RunLumi[2])
		e4.Scale(RunLumi[3])
		e1.Add(e2)
		e1.Add(e3)
		e1.Add(e4)
		ge1 = filein1.Get("RA2bin_%s_%s_%s_MC2016_fast_SLe-genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
		ge1 = filein1.Get("RA2bin_%s_%s_%s_MC2016_fast_SLe-genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
		ge2 = filein2.Get("RA2bin_%s_%s_%s_MC2017_fast_SLe-genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
		ge3 = filein3.Get("RA2bin_%s_%s_%s_MC2018_fast_SLe-genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
		ge4 = filein4.Get("RA2bin_%s_%s_%s_MC2018HEM_fast_SLe-genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
		gm1 = filein1.Get("RA2bin_%s_%s_%s_MC2016_fast_SLm-genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
		ge1.Add(gm1);
		gm2 = filein2.Get("RA2bin_%s_%s_%s_MC2017_fast_SLm-genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
		ge2.Add(gm2);
		gm3 = filein3.Get("RA2bin_%s_%s_%s_MC2018_fast_SLm-genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
		ge3.Add(gm3);
		gm4 = filein4.Get("RA2bin_%s_%s_%s_MC2018HEM_fast_SLm-genMHT"%(options.model,int(mGo[m]), int(mLsp[m])))
		ge4.Add(gm4);
		ge1.Scale(RunLumi[0])
		ge2.Scale(RunLumi[1])
		ge3.Scale(RunLumi[2])
		ge4.Scale(RunLumi[3])
		ge1.Add(e2)
		ge1.Add(e3)
		ge1.Add(e4)
	
		FastSIMCalib=(t1.Integral()+g1.Integral())/2.0
		SLCalib=(ge4.Integral()+e1.Integral())/2.0
		SignifScan.SetPoint(SignifScan.GetN(),mGo[m], mLsp[m],((FastSIMCalib-SLCalib))/(TotalLumi*float(dictXsec.get(mGo[m]))))
	else:
		SignifScan.SetPoint(SignifScan.GetN(),mGo[m], mLsp[m],((t1.Integral()+g1.Integral())/2.0)/(TotalLumi*float(dictXsec.get(mGo[m]))))
  
#GetHistogram():By default returns a pointer to the Delaunay histogram. If fHistogram doesn't exist, books the 2D histogram fHistogram with a margin around the hull. Calls TGraphDelaunay::Interpolate at each bin centre to build up an interpolated 2D histogram. 
#Note that h* histograms are not used in the code as such anywhere.
SignifScan.SetNpx(152)
SignifScan.SetNpy(160)
hSignif=SignifScan.GetHistogram()

fileOut.cd()
hSignif.Write("histoEfff")

#fileOut.Write()
#c.Print("test_MassContoursSmooth.pdf")
fileOut.Close()
#if hlim is None: print "NONE"
#time.sleep(60)
