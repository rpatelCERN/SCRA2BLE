from ROOT import *
import numpy as np
import mmap
import time
import sys
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--model", dest="model", default = "T1tttt",help="SMS model", metavar="model")
parser.add_option("--xsec", dest="xsec", default = "LatestGluGluNNLO.txt",help="SMS model", metavar="xsec")
parser.add_option("--idir", dest="idir", default = "/eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/",help="input path", metavar="idir")
(options, args) = parser.parse_args()
flist=open("listofFiles%s.txt" %options.model, 'r')
#fgluxsec=open("LatestXsecGluGlu.txt", 'r')
dictXsec={}
dictXsecUnc={}
with open('%s' %options.xsec, 'r') as input:
#with open('LatestSquarkNNLO.txt', 'r') as input:
#with open('LatestSbottomStopNNLO.txt', 'r') as input:
        for line in input:
                elements = line.rstrip().split("|")
                dictXsec[int(elements[1])]=elements[2]
                dictXsecUnc[int(elements[1])]=elements[3]
                #print elements
mGo=[]
mLsp=[]
MissMgo=[]
MissMLsp=[]
limit=[]
fileOut=TFile("MassScan%s.root" %options.model, "RECREATE")
PointsFilled=TH2D("PointsFilled", "", 76,600,2500,60, 0,1500)
for line in flist:
        fname=line.split('_')
        mGo.append(float(fname[2]))
        end=fname[3].split('.')
        mLsp.append(float(end[0]))
#print len(mLsp)
MuScan=TGraph2D()
MuScan.SetName("MuScan")
MuScanXsec=TGraph2D()
MuScanXsec.SetName("MuScanXsec")
MuScanXsecExp=TGraph2D()
MuScanXsecExp.SetName("MuScanXsecExp")
MuScanSup=TGraph2D()
MuScanSup.SetName("MuScanSup")
MuScanSdn=TGraph2D()
MuScanSdn.SetName("MuScanSdn")
MuScanObs=TGraph2D()
MuScanObs.SetName("MuScanObs")
MuScanObsSup=TGraph2D()
MuScanObsSup.SetName("MuScanObsSup")
MuScanObsSdn=TGraph2D()
MuScanObsSdn.SetName("MuScanObsSdn")
MuScanSup2=TGraph2D()
MuScanSup2.SetName("MuScanSup2")
MuScanSdn2=TGraph2D()
MuScanSdn2.SetName("MuScanSdn2")

for m in range(len(mGo)):
    	#if sys.argv[1]=="T1qqqq" and mGo[m]<400: continue
	filein=TFile(options.idir+"results_%s_%d_%d.root" %(options.model,int(mGo[m]), int(mLsp[m])))
	t = filein.Get("results")
	if not t:
		MissMgo.append(mGo[m])
		MissMLsp.append(mLsp[m]) 
		continue
	if(mGo[m]%5!=0):continue
	#if mGo[m]<500:continue
	#if(mGo[m]>800):continue
        #if(mGo[m]-mLsp[m]>300):continue
        #if(mGo[m]-mLsp[m]!=150):continue
	t.GetEntry(0)
	print mGo[m]
	ExpUL= t.limit_exp #* float(dictXsec.get(mGo[m]))
	ExpULXSec= t.limit_exp* float(dictXsec.get(mGo[m]))
	ExpULSigmaUp=t.limit_p1s #*float(dictXsec.get(mGo[m]))
    	ExpULSigmaDn=t.limit_m1s #*float(dictXsec.get(mGo[m]))
	ExpULSigma2Up=t.limit_p2s #*float(dictXsec.get(mGo[m]))
    	ExpULSigma2Dn=t.limit_m2s #*float(dictXsec.get(mGo[m]))
	ObsUL=t.limit_obs#*float(dictXsec.get(mGo[m]))
	shiftUp=1.0/(1-(float(dictXsecUnc.get(mGo[m]))/100.));
	shiftDn=1.0/(1+(float(dictXsecUnc.get(mGo[m]))/100.));
	ObsULDn=shiftDn*ObsUL
	ObsULUp=shiftUp*ObsUL
	MuScan.SetPoint(MuScan.GetN(), mGo[m], mLsp[m], ExpUL)
	MuScanSup2.SetPoint(MuScanSup.GetN(), mGo[m], mLsp[m], ExpULSigma2Up)
    	MuScanSdn2.SetPoint(MuScanSdn.GetN(), mGo[m], mLsp[m], ExpULSigma2Dn)
	MuScanSup.SetPoint(MuScanSup.GetN(), mGo[m], mLsp[m], ExpULSigmaUp)
    	MuScanSdn.SetPoint(MuScanSdn.GetN(), mGo[m], mLsp[m], ExpULSigmaDn)
	MuScanObs.SetPoint( MuScanObs.GetN(), mGo[m], mLsp[m], ObsUL)
	MuScanObsSup.SetPoint( MuScanObsSup.GetN(), mGo[m], mLsp[m], ObsULUp)
    	MuScanObsSdn.SetPoint( MuScanObsSdn.GetN(), mGo[m], mLsp[m], ObsULDn)
	MuScanXsec.SetPoint(MuScanXsec.GetN(), mGo[m], mLsp[m],ObsUL*float(dictXsec.get(mGo[m])))
	MuScanXsecExp.SetPoint(MuScanXsecExp.GetN(), mGo[m], mLsp[m],ExpULXSec)
        PointsFilled.Fill( mGo[m], mLsp[m],ExpUL)	
MuScan.SetName("MuScan")
MuScan.SetNpx(128)
MuScan.SetNpy(160)
MuScanSup.SetNpx(128)
MuScanSup.SetNpx(160)
MuScanSdn.SetNpx(128)
MuScanSdn.SetNpx(160)
MuScanObs.SetNpx(128)
MuScanObs.SetNpy(160)
MuScanObsSup.SetNpx(128)
MuScanObsSup.SetNpy(160)
MuScanObsSdn.SetNpx(128)
MuScanObsSdn.SetNpy(160)
MuScanSup2.SetNpx(128)
MuScanSup2.SetNpy(160)
MuScanSdn2.SetNpx(128)
MuScanSdn2.SetNpy(160)
MuScanXsec.SetNpx(128)
MuScanXsec.SetNpy(160)
MuScanXsecExp.SetNpx(128)
MuScanXsecExp.SetNpy(160)

hExplim=MuScan.GetHistogram()
hExplimSup=MuScanSup.GetHistogram()
hExplimSdn=MuScanSdn.GetHistogram()
hObslim=MuScanObs.GetHistogram()
hObslimSup=MuScanObsSup.GetHistogram()
hObslimSdn=MuScanObsSdn.GetHistogram()
hExplimSup2=MuScanSup2.GetHistogram()
hExplimSdn2=MuScanSdn2.GetHistogram()
MassScan2D=MuScanXsec.GetHistogram()
MassScan2DExp=MuScanXsecExp.GetHistogram()
c=TCanvas("c","",800,800);
MuScan.Draw("colz")
MuScanSup.Draw("colz")
MuScanSdn.Draw("colz")
MuScanObs.Draw("colz")
MuScanObsSup.Draw("colz")
MuScanObsSdn.Draw("colz")
ExpLim=TGraph()
ExpLim.SetName("ExpLim")
#PointsFilled.SetName("PointsFilled")
#PointsFilled.Draw("colz");
ExpLim= MuScan.GetContourList(1.0);
ExpLimSup= MuScanSup.GetContourList(1.0);
ExpLimSdn= MuScanSdn.GetContourList(1.0);
ExpLimSup2= MuScanSup2.GetContourList(1.0);
ExpLimSdn2= MuScanSdn2.GetContourList(1.0);
ObsLim= MuScanObs.GetContourList(1.0);
ObsLimSup= MuScanObsSup.GetContourList(1.0);
ObsLimSdn= MuScanObsSdn.GetContourList(1.0);
#CrossCheckExpLim=PointsFilled.GetContourList(1.0)
MuScan.Draw("colz")

fileOut.cd()
ExpLim.Write("ExpLim")
ExpLimSup2.Write("ExpLimSup2")
ExpLimSdn2.Write("ExpLimSdn2")
ExpLimSup.Write("ExpLimSup")
ExpLimSdn.Write("ExpLimSdn")
ObsLim.Write("ObsLim")
ObsLimSup.Write("ObsLimSup")
ObsLimSdn.Write("ObsLimSdn")
MassScan2D.Write("MassScan2D")
MassScan2DExp.Write("MassScan2DExp")
PointsFilled.Write("PointsFilled")
#CrossCheckExpLim.Write("CrossCheckExpLim")
fileOut.Write()
c.Print("test.pdf")
fileOut.Close()
#if hlim is None: print "NONE"
#time.sleep(60)
