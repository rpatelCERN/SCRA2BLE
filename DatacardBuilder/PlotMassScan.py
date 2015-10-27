from ROOT import *
import numpy as np
import tdrstyle
tdrstyle.setTDRStyle()

# flist=open("listofFiles.txt", 'r')
# mGo=[]
# mLsp=[]
# limit=[]
# for line in flist:
# 	fname=line.split('_')
# 	mGo.append(float(fname[2]))
# 	end=fname[3].split('.')
# 	mLsp.append(float(end[0]))

ROOT.gStyle.SetPadLeftMargin(0.16);
ROOT.gStyle.SetPadRightMargin(0.20);
ROOT.gStyle.SetPadTopMargin(0.10);
ROOT.gStyle.SetPalette(1);

f = TFile("inputHistograms/histograms_1.3fb/fastsimSignalScan/RA2bin_signal.root");
names = [k.GetName() for k in f.GetListOfKeys()]

mGo=[]
mLsp=[]
limit=[]
for n in names:
	parse=n.split('_')
	tmpm = float(parse[2])
	#if tmpm == 1075 or tmpm == 1025 or tmpm == 625 or tmpm == 675 or tmpm == 725 or tmpm == 775 or tmpm == 825 or tmpm == 875 or tmpm == 925 or tmpm == 975 or tmpm == 1125 or tmpm == 1175: continue;
	mGo.append(float(parse[2]))
	mLsp.append(float(parse[3]))
	print parse;


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
h2_MassScan=TH2F("h2_MassScan", "Mass Scan T1bbbb",     len(mGoRangeArray)-1, mGoRangeArray, len(mLspRangeArray)-1, mLspRangeArray)
h2_MassScanMu=TH2F("h2_MassScanMu", "Mass Scan T1bbbb", len(mGoRangeArray)-1, mGoRangeArray, len(mLspRangeArray)-1, mLspRangeArray)
print len(mGoRangeArray)-1, mGoRangeArray
print len(mLspRangeArray)-1, mLspRangeArray

idir = "/eos/uscms/store/user/ntran/SUSY/statInterp/scanOutput/";
for m in range(len(mGo)):
	filein=TFile(idir+"results_T1bbbb_%d_%d.root" %(int(mGo[m]), int(mLsp[m])))
	#print "results_T1bbbb_%d_%d.root" %(int(mGo[m]), int(mLsp[m]))
	t = filein.Get("results")
	t.GetEntry(0)
	h2_MassScan.Fill(mGo[m],mLsp[m],t.limit)
	h2_MassScanMu.Fill(mGo[m],mLsp[m],t.fittedMu)
	print mGo[m], mLsp[m],t.limit

c1=TCanvas("c1", "", 1600,1000)
h2_MassScan.GetXaxis().SetTitle(" M_{g} ")
h2_MassScan.GetYaxis().SetTitle(" m_{ #chi } ")
h2_MassScan.SetMaximum(20);
# fout=TFile("test.root", 'recreate')
# h2_MassScan.Write()
# h2_MassScanMu.Write()
# h2_MassScan.Smooth();
h2_MassScan.Draw("colz")
c1.Print("testMassScan.pdf")
