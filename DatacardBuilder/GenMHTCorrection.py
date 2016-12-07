from ROOT import *

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
