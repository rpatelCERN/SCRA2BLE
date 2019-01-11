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
with open('LatestXsecSqtSqt.txt', 'r') as input:
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
names = next(os.walk("/eos/uscms/store/user/rgp230/SUSY/CheckYields/Run2ProductionV12/fastsimSignal%s/" %options.model))[2]
#names = next(os.walk("/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/"))[2]

for n in names:
	print "nList ",n
	parse=n.split('_')
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
idir = "/eos/uscms/store/user/rgp230/SUSY/CheckYields/Run2ProductionV12/fastsimSignal%s/" %options.model #"/eos/uscms/store/user/arane/Limits_T1tttt/";
for m in range(len(mGo)):
#	if(mGo[m]==1300 and mLsp[m]==200):
		#print "Check if this file is really empty before execution"
#		continue;
    	#if sys.argv[1]=="T1qqqq" and mGo[m]<400: continue
	filein=TFile(idir+"RA2bin_signal_%s_%s_%s_fast.root" %(options.model,int(mGo[m]), int(mLsp[m])))
	if dictXsec.get(mGo[m])==None:continue
	print mGo[m],dictXsec.get(mGo[m])
	t = filein.Get("RA2bin_%s_%s_%s_fast_nominal"%(options.model,int(mGo[m]), int(mLsp[m])))
	SignifScan.SetPoint(SignifScan.GetN(),mGo[m], mLsp[m],t.Integral()/(35862.824*float(dictXsec.get(mGo[m]))))

#GetHistogram():By default returns a pointer to the Delaunay histogram. If fHistogram doesn't exist, books the 2D histogram fHistogram with a margin around the hull. Calls TGraphDelaunay::Interpolate at each bin centre to build up an interpolated 2D histogram. 
#Note that h* histograms are not used in the code as such anywhere.
SignifScan.SetNpx(128)
SignifScan.SetNpy(160)
hSignif=SignifScan.GetHistogram()

fileOut.cd()
hSignif.Write("histoEfff")

#fileOut.Write()
#c.Print("test_MassContoursSmooth.pdf")
fileOut.Close()
#if hlim is None: print "NONE"
#time.sleep(60)
