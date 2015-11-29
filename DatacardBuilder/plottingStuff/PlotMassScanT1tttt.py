from ROOT import *
import numpy as np
import mmap

flist=open("listofFilesT1tttt.txt", 'r')
#fgluxsec=open("LatestXsecGluGlu.txt", 'r')
dictXsec={}
dictXsecUnc={}
with open('LatestXsecGluGlu.txt', 'r') as input:	
	for line in input:
		elements = line.rstrip().split("|")
		dictXsec[int(elements[1])]=elements[2]
		dictXsecUnc[int(elements[1])]=elements[3]
		print elements
		#dictlist.append(dict(zip(elements[0], elements[1:2])))
#print dictXsec.get("1200"),dictXsecUnc.get("1200")
mGo=[]
mLsp=[]
limit=[]
for line in flist:
	fname=line.split('_')
	mGo.append(float(fname[2]))
	end=fname[3].split('.')
	mLsp.append(float(end[0]))
#unique values
increments=[25,50,100]
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

ftemplate=TFile("T1bbbb_results.root")
#MassScanTempl=ftemplate.Get("hXsec_exp_corr")
#MassScanTempl.GetYaxis().SetRangeUser(600,2000)
#MassScanTempl.GetYaxis().SetRangeUser(0,2000)
#MassScanTempl.Reset()

#h2_MassScan=MassScanTempl.Clone("h2_MassScan");
#h2_MassScanMu=MassScanTempl.Clone("h2_MassScanMu");
#h2_MassScanObs=MassScanTempl.Clone("h2_MassScanObs");
#h2_MassScanSup=MassScanTempl.Clone("h2_MassScanSup");
#h2_MassScanSdn=MassScanTempl.Clone("h2_MassScanSdn");
h2_MassScanMu=TH2F("h2_MassScanMu", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)

h2_MassScan=TH2F("h2_MassScan", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)
h2_MassScanObs=TH2F("h2_MassScanObs", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)
h2_MassScanSup=TH2F("h2_MassScanSup", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)
h2_MassScanSdn=TH2F("h2_MassScanSdn", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)

h2_MassScanXsec=TH2F("h2_MassScanXsec", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)
h2_MassScanObsXsec=TH2F("h2_MassScanObsXsec", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)
h2_MassScanSupXsec=TH2F("h2_MassScanSupXsec", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)
h2_MassScanSdnXsec=TH2F("h2_MassScanSdnXsec", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)

h2_MassScanObsSup=TH2F("h2_MassScanObsSup", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)
h2_MassScanObsSdn=TH2F("h2_MassScanObsSdn", "Mass Scan T1bbbb", 64, 400, 2000, 80,0,2000)

for m in range(len(mGo)):
	filein=TFile("results_T1tttt_%d_%d.root" %(int(mGo[m]), int(mLsp[m])))
	#print "results_T1bbbb_%d_%d.root" %(int(mGo[m]), int(mLsp[m]))
	t = filein.Get("results")
	t.GetEntry(0)
	ExpUL= t.limit_exp * float(dictXsec.get(mGo[m]))
	ExpULSigmaUp=t.limit_p1s *float(dictXsec.get(mGo[m]))
        ExpULSigmaDn=t.limit_m1s *float(dictXsec.get(mGo[m]))
	ObsUL=t.limit_obs*float(dictXsec.get(mGo[m]))
	shiftUp=1.0/(1-(float(dictXsecUnc.get(mGo[m]))/100.));
        shiftDn=1.0/(1+(float(dictXsecUnc.get(mGo[m]))/100.));
	if mGo[m]<1100 and mLsp[m]<200: 
		#print mGo[m],mLsp[m]	
		for i in range(0,4):
			for j in range(0,4):
                                h2_MassScan.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5,t.limit_exp)
                                h2_MassScanObs.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs)
                                h2_MassScanSup.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_p1s)
                                h2_MassScanSdn.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_m1s)
				h2_MassScanObsSup.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs*shiftUp)
				h2_MassScanObsSdn.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs*shiftDn)
				h2_MassScanXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5,ExpUL)
				h2_MassScanObsXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ObsUL)
				h2_MassScanSupXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ExpULSigmaUp)
				h2_MassScanSdnXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ExpULSigmaDn)
		continue
	if not (mGo[m]<1100 and mLsp[m]<200) and ((mLsp[m]<1200 and mGo[m]<1600)):
	     if (mLsp[m]<=200 and mGo[m]>=1100) or mGo[m]-mLsp[m]>=250:
		 for i in range(0,2):
                        for j in range(0,2):
                                h2_MassScan.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5,t.limit_exp)
                                h2_MassScanObs.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs)
                                h2_MassScanSup.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_p1s)
                                h2_MassScanSdn.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_m1s)
				h2_MassScanObsSup.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs*shiftUp)
				h2_MassScanObsSdn.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs*shiftDn)		

                                h2_MassScanXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5,ExpUL)
                                h2_MassScanObsXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ObsUL)
                                h2_MassScanSupXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ExpULSigmaUp)
                                h2_MassScanSdnXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ExpULSigmaDn)				
	     else:
		h2_MassScanXsec.Fill(mGo[m]+(0.5),mLsp[m]+(0.5),ExpUL)
                h2_MassScanObsXsec.Fill(mGo[m]+(0.5),mLsp[m]+(0.5), ObsUL)
                h2_MassScanSupXsec.Fill(mGo[m]+(0.5),mLsp[m]+(0.5), ExpULSigmaUp)
                h2_MassScanSdnXsec.Fill(mGo[m]+(0.5),mLsp[m]+(0.5), ExpULSigmaDn)

		h2_MassScan.Fill(mGo[m]+(0.5),mLsp[m]+(0.5),t.limit_exp)
                h2_MassScanObs.Fill(mGo[m]+(0.5),mLsp[m]+(0.5), t.limit_obs)
                h2_MassScanObsSup.Fill(mGo[m]+(0.5),mLsp[m]+(0.5), t.limit_obs*shiftUp)
                h2_MassScanObsSdn.Fill(mGo[m]+(0.5),mLsp[m]+(0.5), t.limit_obs*shiftDn)
                h2_MassScanSup.Fill(mGo[m]+(0.5),mLsp[m]+(0.5), t.limit_p1s)
                h2_MassScanSdn.Fill(mGo[m]+(0.5),mLsp[m]+(0.5), t.limit_m1s)

	     continue
	if mLsp[m]>=1250 or (mLsp[m]<=200 and mGo[m]>=1100):
		for i in range(0,2):
			for j in range(0,2):
				h2_MassScanXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5,ExpUL)
				h2_MassScanObsXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ObsUL)
				h2_MassScanSupXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ExpULSigmaUp)
				h2_MassScanSdnXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ExpULSigmaDn)

                                h2_MassScan.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5,t.limit_exp)
                                h2_MassScanObs.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs)
                                h2_MassScanSup.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_p1s)
                                h2_MassScanSdn.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_m1s)
				h2_MassScanObsSup.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs*shiftUp)
				h2_MassScanObsSdn.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs*shiftDn)
		continue
	#print "Beyond Continue"
	for i in range(0,2):
                 for j in range(0,2):
                                h2_MassScanXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5,ExpUL)
                                h2_MassScanObsXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ObsUL)
                                h2_MassScanSupXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ExpULSigmaUp)
                                h2_MassScanSdnXsec.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, ExpULSigmaDn)

                                h2_MassScan.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5,t.limit_exp)
                                h2_MassScanObs.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs)
                                h2_MassScanSup.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_p1s)
                                h2_MassScanSdn.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_m1s)
                                h2_MassScanObsSup.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs*shiftUp)
                                h2_MassScanObsSdn.Fill(mGo[m]+(i*25)+0.5,mLsp[m]+(j*25)+0.5, t.limit_obs*shiftDn)		

c1=TCanvas("c1", "", 1000,1000)
fout=TFile("testT1tttt.root", 'recreate')
h2_MassScanXsec.Write()
h2_MassScanObsXsec.Write()
h2_MassScanSupXsec.Write()
h2_MassScanSdnXsec.Write()

h2_MassScan.Write()
h2_MassScanObs.Write()
h2_MassScanObsSup.Write()
h2_MassScanObsSdn.Write()
h2_MassScanSup.Write()
h2_MassScanSdn.Write()
h2_MassScanXsec.Draw("colz")
c1.Print("testMassScan.pdf")
