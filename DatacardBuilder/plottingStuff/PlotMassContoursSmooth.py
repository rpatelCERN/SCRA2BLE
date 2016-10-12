from ROOT import *
import numpy as np
import mmap
import time
import sys
flist=open("listofFiles%s.txt" %sys.argv[1], 'r')
dictXsec={}
dictXsecUnc={}

with open('LatestXsecGluGlu.txt', 'r') as input:
#with open('LatestXsecSqtSqt.txt', 'r') as input:
#with open('LatestXsecSquSqu.txt', 'r') as input:
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

for line in flist:
        fname=line.split('_')
        mGo.append(float(fname[2]))
        end=fname[3].split('.')
        mLsp.append(float(end[0]))
#print len(mLsp)
#SignifScan=TGraph2D()
#SignifScan.SetName("SignifScan")
#histoSignifScan=TH2D("histoSignifScan", "Signif. Scan (#sigma) ", 100, 0, 2500, 64,0,1600)
MuScan=TGraph2D()
MuScan.SetName("MuScan")
MuScanXsec=TGraph2D()
MuScanXsec.SetName("MuScanXsec")
MuScanExpXsec=TGraph2D()
MuScanExpXsec.SetName("MuScanExpXsec")

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
histoMuObs=TH2D("histoMuObs", "U.L. Obs on #mu ", 100, 0, 2500, 64,0,1600)
histoMuExp=TH2D("histoMuExp", "U.L. Obs on #mu ", 100, 0, 2500, 64,0,1600)
for m in range(len(mGo)):
	filein=TFile("results_%s_%d_%d_mu0.0.root" %(sys.argv[1],int(mGo[m]), int(mLsp[m])))
	if not filein:continue
	if filein.IsZombie():continue
	t = filein.Get("results")
	if not t:
		MissMgo.append(mGo[m])
		MissMLsp.append(mLsp[m]) 
		continue
	t.GetEntry(0)
	
	ExpUL= t.limit_exp #* float(dictXsec.get(mGo[m]))
	ObsULXSec= t.limit_obs * float(dictXsec.get(mGo[m]))
	ExpULXSec= t.limit_exp * float(dictXsec.get(mGo[m]))

	#print float(dictXsec.get(mGo[m])),ExpULXSec
	ExpULSigmaUp=t.limit_p1s #*float(dictXsec.get(mGo[m]))
    	ExpULSigmaDn=t.limit_m1s #*float(dictXsec.get(mGo[m]))
	ObsUL=t.limit_obs#*float(dictXsec.get(mGo[m]))
	histoMuObs.Fill(mGo[m], mLsp[m], t.limit_obs)
	histoMuExp.Fill(mGo[m], mLsp[m],ExpUL)
	shiftUp=1.0/(1-(float(dictXsecUnc.get(mGo[m]))/100.));
	#if mGo[m]<550: 
	#print dictXsecUnc.get(mGo[m]), mGo[m]
	shiftDn=1.0/(1+(float(dictXsecUnc.get(mGo[m]))/100.));
	ObsULDn=shiftDn*ObsUL
	ObsULUp=shiftUp*ObsUL
	#if sys.argv[1]=="T1qqqq":
	#SignifScan.SetPoint(SignifScan.GetN(),mGo[m], mLsp[m],t.significance)
	#histoSignifScan.Fill(mGo[m], mLsp[m],t.significance)
        MuScan.SetPoint(MuScan.GetN(), mGo[m], mLsp[m], ExpUL)
        MuScanSup.SetPoint(MuScanSup.GetN(), mGo[m], mLsp[m], ExpULSigmaUp)
        MuScanSdn.SetPoint(MuScanSdn.GetN(), mGo[m], mLsp[m], ExpULSigmaDn)
        MuScanObs.SetPoint( MuScanObs.GetN(), mGo[m], mLsp[m], ObsUL)
        MuScanObsSup.SetPoint( MuScanObsSup.GetN(), mGo[m], mLsp[m], ObsULUp)
        MuScanObsSdn.SetPoint( MuScanObsSdn.GetN(), mGo[m], mLsp[m], ObsULDn)
        MuScanXsec.SetPoint(MuScanXsec.GetN(), mGo[m], mLsp[m],ObsULXSec)
        MuScanExpXsec.SetPoint(MuScan.GetN(), mGo[m], mLsp[m], ExpULXSec)

MuScan.SetName("MuScan")
#SignifScan.SetNpx(128)
#SignifScan.SetNpy(160)
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
MuScanExpXsec.SetNpx(128)
MuScanExpXsec.SetNpy(160)
#hSignif=SignifScan.GetHistogram()
hExplim=MuScan.GetHistogram()
hExplimSup=MuScanSup.GetHistogram()
hExplimSdn=MuScanSdn.GetHistogram()
hObslim=MuScanObs.GetHistogram()
hObslimSup=MuScanObsSup.GetHistogram()
hObslimSdn=MuScanObsSdn.GetHistogram()
MassScan2D=MuScanXsec.GetHistogram()
MassScan2DExp=MuScanExpXsec.GetHistogram()
c=TCanvas("c","",800,800);
MuScan.Draw("colz")
MuScanSup.Draw("colz")
MuScanSdn.Draw("colz")
MuScanObs.Draw("colz")
MuScanObsSup.Draw("colz")
MuScanObsSdn.Draw("colz")
ExpLim=TGraph()
ExpLim.SetName("ExpLim")

ExpLim= MuScan.GetContourList(1.0);
ExpLimSup= MuScanSup.GetContourList(1.0);
ExpLimSdn= MuScanSdn.GetContourList(1.0);
ObsLim= MuScanObs.GetContourList(1.0);
ObsLimSup= MuScanObsSup.GetContourList(1.0);
ObsLimSdn= MuScanObsSdn.GetContourList(1.0);
MuScan.Draw("colz")
fileOut=TFile("MassScan%s.root" %sys.argv[1], "RECREATE")

ExpLim.Write("ExpLim")
ExpLimSup.Write("ExpLimSup")
ExpLimSdn.Write("ExpLimSdn")
ObsLim.Write("ObsLim")
ObsLimSup.Write("ObsLimSup")
ObsLimSdn.Write("ObsLimSdn")
MassScan2D.Write("MassScan2D")
histoMuExp.Write("histoMuExp");
histoMuObs.Write("histoMuObs");
MassScan2DExp.Write("MassScan2DExp")
#hSignif.Write("MassScanSignif")
#histoSignifScan.Write("histoSignif")
#fileOut.Write()
#c.Print("test.pdf")
fileOut.Close()
print MissMgo, MissMLsp 
#if hlim is None: print "NONE"
#time.sleep(60)
