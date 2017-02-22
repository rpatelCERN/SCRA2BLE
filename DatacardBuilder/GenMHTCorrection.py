from ROOT import *
'''
def genMHTCorr(signaldirtag,signaltag,lumi):
	        signalGenGen_file =TFile(signaldirtag+"/RA2bin_signal_genMHT.root");
                signalRegion_sigGen        =signalGenGen_file.Get(signaltag);
                signalRegion_sigGen.Scale(lumi*1000)
		signal_file =TFile(signaldirtag+"/RA2bin_signal.root");
		signalRegion_sigHist = signal_file.Get(signaltag);
		signalRegion_sigHist.Scale(lumi*1000)
		signalCorrHist=signalRegion_sigHist.Clone()
		#HERE YOU CAN CORRECT FOR SIGNAL CONTAMINTION TO DO RISHI
		for i in range(1,signalRegion_sigHist.GetNbinsX()+1):
			signalCorrHist.SetBinContent(i,(signalRegion_sigHist.GetBinContent(i)+signalRegion_sigGen.GetBinContent(i))/2.0)
		signalCorrHist.SetDirectory(0)
		return signalCorrHist
def genMHTSyst(signaldirtag,signaltag,lumi):
		signalGenGen_file =TFile(signaldirtag+"/RA2bin_signal_genMHT.root");
                signalRegion_sigGen        =signalGenGen_file.Get(signaltag);
                signalRegion_sigGen.Scale(lumi*1000)
                signal_file =TFile(signaldirtag+"/RA2bin_signal.root");
                signalRegion_sigHist = signal_file.Get(signaltag);
                signalRegion_sigHist.Scale(lumi*1000)
                signalCorrHist=signalRegion_sigHist.Clone()
                #HERE YOU CAN CORRECT FOR SIGNAL CONTAMINTION TO DO RISHI
                for i in range(1,signalRegion_sigHist.GetNbinsX()+1):
			signalCorrHist.GetXaxis().SetBinLabel(i, "MHTSyst")
                        signalCorrHist.SetBinContent(i,1.0+(abs(signalRegion_sigHist.GetBinContent(i)-signalRegion_sigGen.GetBinContent(i))/2.0))
                signalCorrHist.SetDirectory(0)
		return signalCorrHist
'''
def LeptonCorr(signaldirtag,model,lumi, mGo, mLSP): #Here you can also add the genMHT hist
	signalContamLL_file=TFile("inputHistograms/SignalContamin/LLContamination_%s.root" %model)
	signalContamTau_file=TFile("inputHistograms/SignalContamin/Signal%sHtauContamin.root" %model)
	LLHist=signalContamLL_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
	TauHist=signalContamTau_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
	LLHist.Scale(1000*lumi)
	TauHist.Scale(1000*lumi)
	sms=model+'_%d_%d_fast' %(mGo,mLSP)
        signal_file =TFile(signaldirtag+"/RA2bin_signal_%s.root" %sms);
	signaltag="RA2bin_"+sms;
        signalRegion_sigHist = signal_file.Get(signaltag+"_nominal");
        signalRegion_genHist = signal_file.Get(signaltag+"_genMHT");
	signalRegion_sigHist.Scale(1000*lumi)
	signalRegion_genHist.Scale(1000*lumi)
	signalHistContam=signalRegion_sigHist.Clone("signalHistContam")
	for i in range(1,signalHistContam.GetNbinsX()+1):
		YieldGen=signalRegion_genHist.GetBinContent(i)
		#if signalHistContam.GetBinContent(i)>0.0:
			#YieldGen=signalRegion_genHist.GetBinContent(i)-((TauHist.GetBinContent(i)+LLHist.GetBinContent(i))*signalRegion_genHist.GetBinContent(i)/signalHistContam.GetBinContent(i)) #CORRECT THIS TO BE THE CONTAMINATION RUN OVER GEN
		Yield=signalHistContam.GetBinContent(i)
		Yield=(YieldGen+Yield)/2.0
		Yield=Yield-TauHist.GetBinContent(i)-LLHist.GetBinContent(i)
		if Yield<0: Yield=0;
		signalHistContam.SetBinContent(i, Yield);
	signalHistContam.SetDirectory(0)
	return signalHistContam
	
