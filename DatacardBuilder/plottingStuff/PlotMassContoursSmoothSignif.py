from ROOT import TGraph
from ROOT import TGraph2D
from ROOT import TH2D
from ROOT import TFile
from ROOT import TCanvas
import mmap
import time
import sys
flist=open("listofFiles%s.txt" %sys.argv[1], 'r')
dictXsec={}
dictXsecUnc={}
#with open('LatestGluGluNNLO.txt', 'r') as input:
#with open('LatestSbottomStopNNLO.txt', 'r') as input:
with open('%s' %sys.argv[2], 'r') as input:
#with open('LatestXsecGluGlu.txt', 'r') as input:
##with open('LatestXsecSqtSqt.txt', 'r') as input:
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

for line in flist:
        fname=line.split('_')
        mGo.append(float(fname[2]))
        end=fname[3].split('.')
        mLsp.append(float(end[0]))
print(len(mLsp))
SignifScan=TGraph2D()
SignifScan.SetName("SignifScan")
histoSignifScan=TH2D("histoSignifScan", "Signif. Scan (#sigma) ", 100, 0, 2500, 64,0,1600)
for m in range(len(mGo)):
	filein=TFile("results_%s_%d_%d_mu0.0.root" %(sys.argv[1],int(mGo[m]), int(mLsp[m])))
	if not filein:
	        MissMgo.append(mGo[m])
                MissMLsp.append(mLsp[m])
		continue
	if filein.IsZombie():
                MissMgo.append(mGo[m])
                MissMLsp.append(mLsp[m])
		continue
	t = filein.Get("results")
	if not t:
		MissMgo.append(mGo[m])
		MissMLsp.append(mLsp[m]) 
   		continue
	t.GetEntry(0)
	#if t.significance< -1.2:continue
	#if (mGo[m]-mLsp[m]<750 and mGo[m]-mLsp[m]>400 and t.significance>-0.6):continue
	#if mGo[]==650 and t.significance>0.8: continue
	#if mLsp[m]==1:continue
	#if t.significance<-1.0:continue
	#if mGo[m]-mLsp[m]<225 :continue
	#if mGo[m]>600 and mGo[m]<700 and t.significance>1.0:continue
	#if mGo[m]-mLsp[m]<250 and mGo[m]-mLsp[m]>600 and t.significance<-1.0:continue
	#if t.significance>-0.5 and (mGo[m]-mLsp[m]<275) and mGo[m]<600:continue
	SignifScan.SetPoint(SignifScan.GetN(),mGo[m], mLsp[m],t.significance)
	histoSignifScan.Fill(mGo[m], mLsp[m],t.significance)
        #SignifScan.SetPoint(SignifScan.GetN(),mGo[m], mLsp[m],t.significance)
        #histoSignifScan.Fill(mGo[m], mLsp[m],t.significance)
        #SignifScan.SetPoint(SignifScan.GetN(),mGo[m], mLsp[m],t.significance)
        #histoSignifScan.Fill(mGo[m], mLsp[m],t.significance)
        #SignifScan.SetPoint(SignifScan.GetN(),mGo[m], mLsp[m],t.significance)
        #histoSignifScan.Fill(mGo[m], mLsp[m],t.significance)
	#if mGo[m]==1250 and mLsp[m]<=100:print "%d %d %g " %(mGo[m], mLsp[m],t.significance)
SignifScan.SetNpx(132)
SignifScan.SetNpy(128)
hSignif=SignifScan.GetHistogram()
c=TCanvas("c","",800,800);
fileOut=TFile("MassScan%s.root" %sys.argv[1], "RECREATE")
print MissMgo
print MissMLsp
hSignif.Write("MassScanSignif")
histoSignifScan.Write("histoSignif")
fileOut.Close()
