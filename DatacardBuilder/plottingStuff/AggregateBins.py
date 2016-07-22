from ROOT import *
import os


fbkg=TFile("testCards-allBkgs-SMStt500-7.6-mu0.0/yields.root", "READ")
Data=fbkg.Get("data")
QCD=fbkg.Get("QCD")
Zvv=fbkg.Get("Zvv")
LL=fbkg.Get("LL")
tau=fbkg.Get("tau")
sig=fbkg.Get("sig")

flabels=TFile("inputHistograms/FullSim/RA2bin_signal.root", "READ")
dictAggBins={}
template=flabels.Get("RA2bin_SMStttt1500")
Region1Labels=[]
Region1bins=[]
Region2Labels=[]
Region2bins=[]
Region3Labels=[]
Region3bins=[]
Region4Labels=[]
Region4bins=[]
Region5Labels=[]
Region5bins=[]
Region6Labels=[]
Region6bins=[]
Region7Labels=[]
Region7bins=[]
Region8Labels=[]
Region8bins=[]
Region9Labels=[]
Region9bins=[]
Region10Labels=[]
Region10bins=[]
Region11Labels=[]
Region11bins=[]
Region12Labels=[]
Region12bins=[]

for i in range(0,160):
	label=template.GetXaxis().GetBinLabel(i+1)
	parse=label.split("_")
	if "BTags0" in parse[1]:
		if "HT6" in parse[3] or "HT7" in parse[3] or "HT8" in parse[3] or "HT9" in parse[3]:
				Region1Labels.append(label)
				Region1bins.append(i)	
		if "HT9" in parse[3]:
                                Region2Labels.append(label)
                                Region2bins.append(i)
		if ("NJets0" not in parse[0]) and ("HT6" in parse[3] or "HT7" in parse[3] or "HT8" in parse[3] or "HT9" in parse[3]):
                                Region3Labels.append(label)
                                Region3bins.append(i)
		if ("NJets0" not in parse[0]) and ("HT9" in parse[3]):
				Region4Labels.append(label)
				Region4bins.append(i)
		if ("NJets3" in parse[0]) and ("HT9" in parse[3]):
				Region5Labels.append(label)
				Region5bins.append(i)
	if "BTags2" in parse[1] or "BTags3" in parse[1]:
		if "HT6" in parse[3] or "HT7" in parse[3] or "HT8" in parse[3] or "HT9" in parse[3]:
                                Region6Labels.append(label)
                                Region6bins.append(i)		
	if "BTags0" not in parse[1]:
		if "HT8" in parse[3] or "HT9" in parse[3]:
                                Region7Labels.append(label)
                                Region7bins.append(i)
	if "NJets0" not in parse[0]:
		 if "BTags3" in parse[1] and ("HT6" in parse[3] or "HT7" in parse[3] or "HT8" in parse[3] or "HT9" in parse[3]):
                                Region8Labels.append(label)
                                Region8bins.append(i)
                 if ("BTags2" in parse[1] or "BTags3" in parse[1]) and ("HT6" in parse[3] or "HT7" in parse[3] or "HT8" in parse[3] or "HT9" in parse[3]):	
                                Region9Labels.append(label)
                                Region9bins.append(i)
	if "NJets3" in parse[0] and "BTags3" in parse[1] and ("HT8" in parse[3] or "HT9" in parse[3]):
                                Region10Labels.append(label)
                                Region10bins.append(i)		
	if ("NJets3" in parse[0] or "NJets2" in parse[0]) and ("BTags0" not in parse[1]):
                                Region11Labels.append(label)
                                Region11bins.append(i)
	if ("NJets0" not in parse[0]) and ("BTags0" not in parse[1])  and ("HT8" in parse[3] or "HT9" in parse[3]):
                                Region12Labels.append(label)
                                Region12bins.append(i)
#open cards
tmpQCD=0
tmpZ=0
tmpsig=0
tmpTau=0
tmpLL=0
tmpData=0
Zbins=[]
sigbins=[]
Taubins=[]
QCDbins=[]
LLbins=[]
Databins=[]
for i in Region1bins:
	tmpLL=tmpLL+LL.GetBinContent(i+1)
	tmpTau=tmpTau+tau.GetBinContent(i+1)
	tmpQCD=tmpQCD+QCD.GetBinContent(i+1)
	tmpZ=tmpZ+Zvv.GetBinContent(i+1)
	tmpsig=tmpsig+sig.GetBinContent(i+1)	
	tmpData=tmpData+Data.GetBinContent(i+1)	
		#for line in fcard:
		#	print line
Zbins.append(tmpZ)
sigbins.append(tmpsig)
Taubins.append(tmpTau)
QCDbins.append(tmpQCD)
LLbins.append(tmpLL)
Databins.append(tmpData)
tmpQCD=0
tmpZ=0
tmpsig=0
tmpTau=0
tmpLL=0
tmpData=0

for i in Region2bins:
        tmpLL=tmpLL+LL.GetBinContent(i+1)
        tmpTau=tmpTau+tau.GetBinContent(i+1)
        tmpQCD=tmpQCD+QCD.GetBinContent(i+1)
        tmpZ=tmpZ+Zvv.GetBinContent(i+1)
        tmpsig=tmpsig+sig.GetBinContent(i+1)
        tmpData=tmpData+Data.GetBinContent(i+1)
                #for line in fcard:
                #       print line
Zbins.append(tmpZ)
sigbins.append(tmpsig)
Taubins.append(tmpTau)
QCDbins.append(tmpQCD)
LLbins.append(tmpLL)
Databins.append(tmpData)
tmpQCD=0
tmpZ=0
tmpsig=0
tmpTau=0
tmpLL=0
tmpData=0
for i in Region3bins:
        tmpLL=tmpLL+LL.GetBinContent(i+1)
        tmpTau=tmpTau+tau.GetBinContent(i+1)
        tmpQCD=tmpQCD+QCD.GetBinContent(i+1)
        tmpZ=tmpZ+Zvv.GetBinContent(i+1)
        tmpsig=tmpsig+sig.GetBinContent(i+1)
        tmpData=tmpData+Data.GetBinContent(i+1)
                #for line in fcard:
                #       print line
Zbins.append(tmpZ)
sigbins.append(tmpsig)
Taubins.append(tmpTau)
QCDbins.append(tmpQCD)
LLbins.append(tmpLL)
Databins.append(tmpData)
tmpQCD=0
tmpZ=0
tmpsig=0
tmpTau=0
tmpLL=0
tmpData=0
for i in Region4bins:
        tmpLL=tmpLL+LL.GetBinContent(i+1)
        tmpTau=tmpTau+tau.GetBinContent(i+1)
        tmpQCD=tmpQCD+QCD.GetBinContent(i+1)
        tmpZ=tmpZ+Zvv.GetBinContent(i+1)
        tmpsig=tmpsig+sig.GetBinContent(i+1)
        tmpData=tmpData+Data.GetBinContent(i+1)
                #for line in fcard:
                #       print line
Zbins.append(tmpZ)
sigbins.append(tmpsig)
Taubins.append(tmpTau)
QCDbins.append(tmpQCD)
LLbins.append(tmpLL)
Databins.append(tmpData)
tmpQCD=0
tmpZ=0
tmpsig=0
tmpTau=0
tmpLL=0
tmpData=0
for i in Region5bins:
        tmpLL=tmpLL+LL.GetBinContent(i+1)
        tmpTau=tmpTau+tau.GetBinContent(i+1)
        tmpQCD=tmpQCD+QCD.GetBinContent(i+1)
        tmpZ=tmpZ+Zvv.GetBinContent(i+1)
        tmpsig=tmpsig+sig.GetBinContent(i+1)
        tmpData=tmpData+Data.GetBinContent(i+1)
                #for line in fcard:
                #       print line
Zbins.append(tmpZ)
sigbins.append(tmpsig)
Taubins.append(tmpTau)
QCDbins.append(tmpQCD)
LLbins.append(tmpLL)
Databins.append(tmpData)
tmpQCD=0
tmpZ=0
tmpsig=0
tmpTau=0
tmpLL=0
tmpData=0
RegionsBins=[]
RegionsBins.append((Region1bins))
RegionsBins.append((Region2bins))
RegionsBins.append((Region3bins))
RegionsBins.append((Region4bins))
RegionsBins.append((Region5bins))
RegionsBins.append((Region6bins))
RegionsBins.append((Region7bins))
RegionsBins.append((Region8bins))
RegionsBins.append((Region9bins))
RegionsBins.append((Region10bins))
RegionsBins.append((Region11bins))
RegionsBins.append((Region12bins))
print RegionsBins[0]
count=0
for binlist in RegionsBins:
	tmpQCD=0
	tmpZ=0
	tmpsig=0
	tmpTau=0
	tmpLL=0
	tmpData=0
	mockCardList=""
	for i in binlist:
        	tmpLL=tmpLL+LL.GetBinContent(i+1)
        	tmpTau=tmpTau+tau.GetBinContent(i+1)
        	tmpQCD=tmpQCD+QCD.GetBinContent(i+1)
        	tmpZ=tmpZ+Zvv.GetBinContent(i+1)
       		tmpsig=tmpsig+sig.GetBinContent(i+1)
        	tmpData=tmpData+Data.GetBinContent(i+1)
		# HARD PART GRAB Nuisances
		'''
		fcard=open("testCards-allBkgs-SMStt500-7.6-mu0.0/card_signal%d.txt" %i, 'r')
		for line in fcard:
				parse=line.split(" ")
				print parse
		'''
		mockCardList=mockCardList+"testCards-allBkgs-SMStt500-7.6-mu0.0/card_signal%d.txt " %i
	os.system("combineCards.py %s >MockNuisanceCombTest%d.txt " %(mockCardList,count))
	count=count+1
	Zbins.append(tmpZ)
	sigbins.append(tmpsig)
	Taubins.append(tmpTau)
	QCDbins.append(tmpQCD)
	LLbins.append(tmpLL)
	Databins.append(tmpData)
print Databins, sigbins, LLbins, Taubins, QCDbins, Zbins
print "Region & Lost Lepton & Tau & Z & QCD &Total & Obs \\\\\ "
for i in range(0,12):
	Total=Zbins[i]+Taubins[i]+QCDbins[i]+ LLbins[i]
	print "%d &  %2.2f & %2.2f & %2.2f & %2.2f & %2.2f & %d " %(i+1, LLbins[i], Taubins[i],Zbins[i], QCDbins[i], Total, Databins[i])
	'''
	fcard=open("MockNuisanceCombTest%d.txt" %i, 'r')
	for line in fcard:
		 parse=line.split(" ")
                 if "rate" in parse[0]:print parse
	'''
