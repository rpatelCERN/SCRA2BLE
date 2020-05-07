from ROOT import *
import os
ZSystematicsSym=["hzvvgJEtrgErr","hzvvgJPurErr","hzvvScaleErr","hzvvDYsysPur","hzvvDYstat","hzvvDYsysKin"]
ZSystematicsASym=["hzvvNbCorrelLow","hzvvNbCorrelUp","hzvvDYMCerrLow","hzvvDYMCerrUp"]
#LLSystematicsList=["LLPlusHadTauTF","DataCSStatistics","LLPlusHadTauTFErr","totalPredBMistagDown_LLPlusHadTau","totalPredJECSysDown_LLPlusHadTau","totalPredMTSysDown_LL","totalPredPDFDown_LLPlusHadTau","totalPredScaleDown_LLPlusHadTau","totalPredEleIDSysDown_LL","totalPredEleIsoSysDown_LL","totalPredEleRecoSysDown_LL","totalPredMuIsoSysDown_LL","totalPredMuIDSysDown_LL","totalPredMuRecoSysDown_LL"]
LLSystematicsList=["LLPlusHadTauBMistag","LLPlusHadTau_muAccSys","LLPlusHadTau_muAccQsquareSys","LL_eleIDSys","LL_eleIsoSys","LL_eleRecoSys","LL_muIsoSys","LL_muIDSys","LL_muRecoSys"]
QCDSystematics=["QCDCore","QCDTail","PredictionUncorrelated"]
MHTHTLabels=["MHT0_HT0","MHT0_HT1", "MHT0_HT2","MHT1_HT3","MHT1_HT4", "MHT1_HT5", "MHT2_HT6", "MHT2_HT7","MHT3_HT8", "MHT3_HT9" ]
MHTLabels=["MHT0","MHT1","MHT2", "MHT3"]
#QCDFile=TFile.Open("../inputHistograms/histograms_137.4fb/QcdPredictionRandS.root","READ")
#QCDUncorrel=QCDFile.Get("PredictionUncorrelated");


for q in QCDSystematics:
	if q is "PredictionUncorrelated":continue
	NuisanceName="%s" %(q)
	cmmd="combine -M MultiDimFit --rMin=-5 --rMax=5  -t -1 --expectSignal 0 --robustFit 1 -n _paramFit_TestImpactsRA2_%s --algo impact --redefineSignalPOIs r -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root  "%(NuisanceName,NuisanceName)
	#os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
	#print #cmmd
#for q in range(1, QCDUncorrel.GetNbinsX()+1):
#	print QCDUncorrel.GetXaxis().GetBinLabel(q)
for j in range(0,5):
	for mht in MHTHTLabels:
		for b in range(0,4):
			#NuisanceName="MTSys_NJets%d_BTags%d_%s" %(j, b,mht)
			NuisanceName="QCDUncorrelNJets%d_BTagsDeepCSV%d_%s" %(j, b,mht)
			cmmd="combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0  -n _paramFit_TestImpactsRA2_%s --rMin=-50 --rMax=50   --algo impact --redefineSignalPOIs r  -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
                	#cmmd="combine -M MultiDimFit --rMin -10 -n _paramFit_TestImpactsRA2_%s --algo impact --redefineSignalPOIs r -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 1 -d allcards.root -t -1 --expectSignal 0" %(NuisanceName,NuisanceName)
			#os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
			#print cmmd
for l in LLSystematicsList:
	NuisanceName="%s" %(l)
	#cmmd="combine -M MultiDimFit --rMin=-1 --rMax=5  -t -1 --expectSignal 0 --robustFit 1 -n _paramFit_TestImpactsRA2_%s --algo impact --redefineSignalPOIs r -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root  "%(NuisanceName,NuisanceName)
	cmmd="combine -M MultiDimFit --rMin=-10 --rMax=10  --robustFit 1 -n _paramFit_TestImpactsRA2_%s --algo impact --redefineSignalPOIs r -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -t -1  --expectSignal 0  -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root  "%(NuisanceName,NuisanceName)
	#os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
	#print cmmd
LostLepUncorrel=["LLPlusHadTauTFErr","LLPlusHadTauEScale", "MTSys"]
#LostLepUncorrel=[ "CSStat"]

for j in range(0,5):
	for mht in MHTHTLabels:
		for b in range(0,4):
			for n in LostLepUncorrel:
				NuisanceName="%s_NJets%d_BTags%d_%s" %(n,j, b,mht)
                        	#NuisanceName="QCDUncorrelNJets%d_BTagsDeepCSV%d_%s" %(j, b,mht)
                        	cmmd="combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0  -n _paramFit_TestImpactsRA2_%s --rMin=-10 --rMax=10 --algo impact --redefineSignalPOIs r -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
				#os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
					
ZCorrel=["zvvgJPurErr","zvvScaleErr"]
for z in ZCorrel:
	NuisanceName="%s" %z
        cmmd="combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0  -n _paramFit_TestImpactsRA2_%s --rMin=-10 --rMax=10   --algo impact --redefineSignalPOIs r  -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
	os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
	print cmmd
for j in range(0,5):
	for mht in MHTHTLabels:
		NuisanceName="zvvNbCorrelLow_NJets%d_%s" %(j,mht)
		cmmd="combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0  -n _paramFit_TestImpactsRA2_%s --rMin=-10 --rMax=10   --algo impact --redefineSignalPOIs r  -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
		os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
		#cmmd="combine -M MultiDimFit --robustFit 1 -n _paramFit_TestImpactsRA2_%s --rMin=-1 --rMax=5 --algo impact --redefineSignalPOIs r -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_600_100-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
		#cmmd= "combineTool.py -M Impacts -P zvvNbCorrelUp_NJets%d_%s   -d allcards.root -m 125 --robustFit 1 --doFits" %(j,mht)
		NuisanceName="zvvgJNobs_NJets%d_%s" %(j,mht)
		cmmd="combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0  -n _paramFit_TestImpactsRA2_%s --rMin=-10 --rMax=10 --algo impact --redefineSignalPOIs r  -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
		print cmmd
		#os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))

for j in range(0,5):
	for mht in MHTHTLabels:
		for b in range(0,4):
			NuisanceName="zvvDYsysKin_NJets%d_BTags%d_%s" %(j,b,mht);
			cmmd="combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0  -n _paramFit_TestImpactsRA2_%s --rMin=-10 --rMax=10   --algo impact --redefineSignalPOIs r  -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
			os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
for j in range(0,5):
	for b in range(0,4):
		NuisanceName="zvvDYsysPur_NJets%d_BTags%d" %(j,b)
		cmmd="combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0  -n _paramFit_TestImpactsRA2_%s --rMin=-10 --rMax=10   --algo impact --redefineSignalPOIs r  -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
		os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
		NuisanceName="zvvDYMCerrLow_NJets%d_BTags%d"%(j,b) 	
		cmmd="combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0  -n _paramFit_TestImpactsRA2_%s --rMin=-10 --rMax=10   --algo impact --redefineSignalPOIs r  -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
		os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
		NuisanceName="zvvDYstat_NJets%d_BTags%d" %(j,b)
		cmmd="combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0  -n _paramFit_TestImpactsRA2_%s --rMin=-10 --rMax=10   --algo impact --redefineSignalPOIs r  -P %s --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_2200_800-137.4-mu0.0/allcards.root "%(NuisanceName,NuisanceName)
		os.system("Qsub -l lnxfarm -o OutPut_LogFile%s -e %s " %(NuisanceName,cmmd))
