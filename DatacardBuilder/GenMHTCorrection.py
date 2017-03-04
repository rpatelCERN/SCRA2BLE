from ROOT import *
def LeptonCorr(signaldirtag,model,lumi, mGo, mLSP): #Here you can also add the genMHT hist
	signalContamLL_file=TFile("inputHistograms/SignalContamin/LLContamination_%s.root" %model)
	signalContamTau_file=TFile("inputHistograms/SignalContamin/Signal%sHtauContamin.root" %model)
	signalContamGenLL_file=TFile("inputHistograms/SignalContamin/LLContamination_genMHT_%s.root" %model)
	signalContamGenTau_file=TFile("inputHistograms/SignalContamin/Signal%sHtauContamin_genMHT.root" %model)
	
	LLHist=TH1D()
	LLGenHist=TH1D()
	TauHist=TH1D()
	TauGenHist=TH1D()
	if "T2" in model:
		LLGenHist=signalContamGenLL_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
		TauGenHist=signalContamGenTau_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
		LLHist=signalContamLL_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
		TauHist=signalContamTau_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
	else:
                LLGenHist=signalContamGenLL_file.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                TauGenHist=signalContamGenTau_file.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                LLHist=signalContamLL_file.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                TauHist=signalContamTau_file.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
	LLGenHist.Scale(1000*lumi)
	TauGenHist.Scale(1000*lumi)
	LLHist.Scale(1000*lumi)
	TauHist.Scale(1000*lumi)
	sms=model+'_%d_%d_fast' %(mGo,mLSP)
	signal_file=TFile.Open(signaldirtag+"/RA2bin_proc_%s.root" %sms);
        #signal_file =TFile(signaldirtag+"/RA2bin_proc_%s.root" %sms);
	signaltag="RA2bin_"+sms;
	print signaltag
        signalRegion_sigHist = signal_file.Get(signaltag+"_nominalOrig");
        signalRegion_genHist = signal_file.Get(signaltag+"_genMHT");
	signalRegion_sigHist.Scale(1000*lumi)
	signalRegion_genHist.Scale(1000*lumi)
	signalHistContam=signalRegion_sigHist.Clone("signalHistContam")
	for i in range(1,signalHistContam.GetNbinsX()+1):
		YieldGen=signalRegion_genHist.GetBinContent(i)
		#if signalHistContam.GetBinContent(i)>0.0:
		print signalRegion_genHist.GetBinContent(i),(TauGenHist.GetBinContent(i)+LLGenHist.GetBinContent(i))
		YieldGen=signalRegion_genHist.GetBinContent(i)-((TauGenHist.GetBinContent(i)+LLGenHist.GetBinContent(i))) #CORRECT THIS TO BE THE CONTAMINATION RUN OVER GEN
		Yield=signalHistContam.GetBinContent(i)-TauHist.GetBinContent(i)-LLHist.GetBinContent(i)
		Yield=(YieldGen+Yield)/2.0
		if Yield<0: Yield=0;
		signalHistContam.SetBinContent(i, Yield);
	signalHistContam.SetDirectory(0)
	return signalHistContam
	
