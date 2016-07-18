from ROOT import *
import numpy as np
import mmap
import time
import sys
flist=open("listofFiles%s.txt" %sys.argv[1], 'r')
#fgluxsec=open("LatestXsecGluGlu.txt", 'r')
dictXsec={}
dictXsecUnc={}
with open('LatestXsecGluGlu.txt', 'r') as input:
        for line in input:
                elements = line.rstrip().split("|")
                dictXsec[int(elements[1])]=elements[2]
                dictXsecUnc[int(elements[1])]=elements[3]
                print elements
mGo=[]
mLsp=[]
MissMgo=[]
MissMLsp=[]
limit=[]
fileOut=TFile("MassScan%s.root" %sys.argv[1], "RECREATE")

for line in flist:
        fname=line.split('_')
        mGo.append(float(fname[2]))
        end=fname[3].split('.')
        mLsp.append(float(end[0]))
print len(mLsp)
MuScan=TGraph2D()
MuScan.SetName("MuScan")
MuScanXsec=TGraph2D()
MuScanXsec.SetName("MuScanXsec")
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
for m in range(len(mGo)):
    	#if sys.argv[1]=="T1qqqq" and mGo[m]<400: continue
	filein=TFile("results_%s_%d_%d.root" %(sys.argv[1],int(mGo[m]), int(mLsp[m])))
	t = filein.Get("results")
	if not t:
		MissMgo.append(mGo[m])
		MissMLsp.append(mLsp[m]) 
		continue
	t.GetEntry(0)
	ExpUL= t.limit_exp #* float(dictXsec.get(mGo[m]))
	ExpULXSec= t.limit_exp* float(dictXsec.get(mGo[m]))
	ExpULSigmaUp=t.limit_p1s #*float(dictXsec.get(mGo[m]))
    	ExpULSigmaDn=t.limit_m1s #*float(dictXsec.get(mGo[m]))
	ObsUL=t.limit_obs#*float(dictXsec.get(mGo[m]))
	shiftUp=1.0/(1-(float(dictXsecUnc.get(mGo[m]))/100.));
	shiftDn=1.0/(1+(float(dictXsecUnc.get(mGo[m]))/100.));
	ObsULDn=shiftDn*ObsUL
	ObsULUp=shiftUp*ObsUL
	if ExpUL<0.000001:continue
	MuScan.SetPoint(MuScan.GetN(), mGo[m], mLsp[m], ExpUL)
	MuScanSup.SetPoint(MuScanSup.GetN(), mGo[m], mLsp[m], ExpULSigmaUp)
    	MuScanSdn.SetPoint(MuScanSdn.GetN(), mGo[m], mLsp[m], ExpULSigmaDn)
	MuScanObs.SetPoint( MuScanObs.GetN(), mGo[m], mLsp[m], ObsUL)
	MuScanObsSup.SetPoint( MuScanObsSup.GetN(), mGo[m], mLsp[m], ObsULUp)
    	MuScanObsSdn.SetPoint( MuScanObsSdn.GetN(), mGo[m], mLsp[m], ObsULDn)
	MuScanXsec.SetPoint(MuScanXsec.GetN(), mGo[m], mLsp[m],ExpULXSec)
	
	'''
	MuScan.SetPoint(m+1, mGo[m], mLsp[m], ExpUL)
	MuScanSup.SetPoint(m+1, mGo[m], mLsp[m], ExpULSigmaUp)
    	MuScanSdn.SetPoint(m+1, mGo[m], mLsp[m], ExpULSigmaDn)
	MuScanObs.SetPoint( m+1, mGo[m], mLsp[m], ObsUL)
	MuScanObsSup.SetPoint(m+1, mGo[m], mLsp[m], ObsULUp)
    	MuScanObsSdn.SetPoint(m+1, mGo[m], mLsp[m], ObsULDn)
	MuScanXsec.SetPoint(m+1, mGo[m], mLsp[m],ExpULXSec)
	'''
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
MuScanXsec.SetNpx(128)
MuScanXsec.SetNpy(160)
hExplim=MuScan.GetHistogram()
hExplimSup=MuScanSup.GetHistogram()
hExplimSdn=MuScanSdn.GetHistogram()
hObslim=MuScanObs.GetHistogram()
hObslimSup=MuScanObsSup.GetHistogram()
hObslimSdn=MuScanObsSdn.GetHistogram()
MassScan2D=MuScanXsec.GetHistogram()
c=TCanvas("c","",800,800);
MuScan.Draw("colz")
MuScanSup.Draw("colz")
MuScanSdn.Draw("colz")
MuScanObs.Draw("colz")
MuScanObsSup.Draw("colz")
MuScanObsSdn.Draw("colz")
ExpLim=TGraph()
ExpLim.SetName("ExpLim")

ExpLim= MuScan.GetContourList(1.);
ExpLimSup= MuScanSup.GetContourList(1.);
ExpLimSdn= MuScanSdn.GetContourList(1.);
ObsLim= MuScanObs.GetContourList(1.);
ObsLimSup= MuScanObsSup.GetContourList(1.);
ObsLimSdn= MuScanObsSdn.GetContourList(1.);

MuScan.Draw("colz")

fileOut.cd()
ExpLim.Write("ExpLim")
ExpLimSup.Write("ExpLimSup")
ExpLimSdn.Write("ExpLimSdn")
ObsLim.Write("ObsLim")
ObsLimSup.Write("ObsLimSup")
ObsLimSdn.Write("ObsLimSdn")
MassScan2D.Write("MassScan2D")

fileOut.Write()
c.Print("test.pdf")
fileOut.Close()
#if hlim is None: print "NONE"
#time.sleep(60)
