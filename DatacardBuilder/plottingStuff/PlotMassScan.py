from ROOT import *
import numpy as np
import os

# flist=open("listofFiles.txt", 'r')
flist = os.listdir('/eos/uscms/store/user/ntran/SUSY/statInterp/scanOutput');

mGo=[]
mLsp=[]
limit=[]
for line in flist:
	fname=line.split('_')
	mGo.append(float(fname[2]))
	end=fname[3].split('.')
	mLsp.append(float(end[0]))
#unique values
mGoRange=mGo[:]
mGoRangeSet=set(mGoRange)
mGoRange=list(mGoRangeSet) #this only has the unique values
mGoRange.sort()
mGoRangeArray=np.asarray(mGoRange)
mLspRange=mLsp[:]
mLspRangeSet=set(mLspRange)
mLspRange=list(mLspRangeSet)
mLspRange.sort()
mLspRangeArray=np.asarray(mLspRange)
h2_MassScan=TH2F("h2_MassScan", "Mass Scan T1bbbb", len(mGoRangeArray)-1, mGoRangeArray, len(mLspRangeArray)-1, mLspRangeArray)
h2_MassScanMu=TH2F("h2_MassScanMu", "Mass Scan T1bbbb", len(mGoRangeArray)-1, mGoRangeArray, len(mLspRangeArray)-1, mLspRangeArray)
print len(mLspRangeArray)-1
print mGoRangeArray
for m in range(len(mGo)):
	#print mGo[m], mLsp[m]
	filein=TFile("results_T1bbbb_%d_%d.root" %(int(mGo[m]), int(mLsp[m])))
	#print "results_T1bbbb_%d_%d.root" %(int(mGo[m]), int(mLsp[m]))
	t = filein.Get("results")
	t.GetEntry(0)
	h2_MassScan.Fill(mGo[m],mLsp[m],t.limit)
	h2_MassScanMu.Fill(mGo[m],mLsp[m],t.fittedMu)
c1=TCanvas("c1", "", 1000,1000)
h2_MassScan.GetXaxis().SetTitle(" M_{g} ")
h2_MassScan.GetYaxis().SetTitle(" m_{ #chi } ")
fout=TFile("test.root", 'recreate')
h2_MassScan.Write()
h2_MassScanMu.Write()
h2_MassScan.Draw("colz")
c1.Print("testMassScan.pdf")
