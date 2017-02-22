import ROOT as root
from ROOT import *
import ROOT
from array import array


finSignal=TFile("../inputHistograms/fastsimSignalT2tt/RA2bin_signal.root", "READ");
SignalT2tt=finSignal.Get("RA2bin_T2tt_175_1_fast")
SignalT2tt.Scale(36300.)
finBkg=TFile("/uscms_data/d2/rgp230/V11DatacardBuilder/CMSSW_8_0_25/src/Analysis/datacards/RA2bin_signal.root");
LL=finBkg.Get("RA2bin_WJet");
LL.Scale(36300.)
#Tau=finBkg.Get("tau");
#LL.Add(Tau);
a_jets = array('d', [2,3,4,6,8,20]);
a_btags = array('d', [0,1,2,3,4]);
BTagsSignal=TH1F('BTagsSignal', ";BTags;Yields", 4,a_btags)
BTagsTTbar=TH1F('BTagsTTbar', ";BTags;Yields", 4,a_btags)
NJetsSignal=TH1F('NJetsSignal', ";NJets;Yields", 5,a_jets)
NJetsTTbar=TH1F('NJetsTTbar', ";NJets;Yields", 5,a_jets)
a_HT= array('d', [300,500,1000,2100]);
a_MHT= array('d', [300,350,500,750,2100]);
MHTSignal=TH1F('MHTSignal', ";MHT;Yields", 4,a_MHT)
MHTTTbar=TH1F('MHTTTbar', ";MHT;Yields", 4,a_MHT)
HTSignal=TH1F('HTSignal', ";HT;Yields", 3,a_HT)
HTTTbar=TH1F('HTTTbar', ";HT;Yields", 3,a_HT)

for i in range(1, 175):
	parse=SignalT2tt.GetXaxis().GetBinLabel(i).split("_")
	print parse
	if "BTags0" in parse[2]: #and ("BTags1" in parse[2] or "BTags2" in parse[2]) :
		BTagsSignal.Fill(0.5, SignalT2tt.GetBinContent(i));
		BTagsTTbar.Fill(0.5, LL.GetBinContent(i))
	if "BTags1" in parse[2]: #and ("BTags1" in parse[2] or "BTags2" in parse[2]) :
		BTagsSignal.Fill(1.5, SignalT2tt.GetBinContent(i));
		BTagsTTbar.Fill(1.5, LL.GetBinContent(i))
	if "BTags2" in parse[2]: #and ("BTags1" in parse[2] or "BTags2" in parse[2]) :
		BTagsSignal.Fill(2.5, SignalT2tt.GetBinContent(i));
		BTagsTTbar.Fill(2.5, LL.GetBinContent(i))
	if "BTags3" in parse[2]: #and ("BTags1" in parse[2] or "BTags2" in parse[2]) :
		BTagsSignal.Fill(3.5, SignalT2tt.GetBinContent(i));
		BTagsTTbar.Fill(3.5, LL.GetBinContent(i))
	if "NJets0" in parse[1]: #and ("BTags1" in parse[2] or "BTags2" in parse[2]) :
		NJetsSignal.Fill(2.5, SignalT2tt.GetBinContent(i));
		NJetsTTbar.Fill(2.5, LL.GetBinContent(i))
	if "NJets1" in parse[1]: #and ("BTags1" in parse[2] or "BTags2" in parse[2]) :
		NJetsSignal.Fill(3.5, SignalT2tt.GetBinContent(i));
		NJetsTTbar.Fill(3.5, LL.GetBinContent(i))
	if "NJets2" in parse[1]: #and ("BTags1" in parse[2] or "BTags2" in parse[2]) :
		NJetsSignal.Fill(5, SignalT2tt.GetBinContent(i));
		NJetsTTbar.Fill(5, LL.GetBinContent(i))
	if "NJets3" in parse[1]: #and ("BTags1" in parse[2] or "BTags2" in parse[2]) :
		NJetsSignal.Fill(7, SignalT2tt.GetBinContent(i));
		NJetsTTbar.Fill(7, LL.GetBinContent(i))
	if "NJets4" in parse[1]: #and ("BTags1" in parse[2] or "BTags2" in parse[2]) :
		NJetsTTbar.Fill(10, LL.GetBinContent(i))
		NJetsSignal.Fill(10, SignalT2tt.GetBinContent(i));
	if "MHT0" in parse[3]:
		MHTTTbar.Fill(325, LL.GetBinContent(i))
		MHTSignal.Fill(325, SignalT2tt.GetBinContent(i));
	if "MHT1" in parse[3]:
		MHTTTbar.Fill(375, LL.GetBinContent(i))
		MHTSignal.Fill(375, SignalT2tt.GetBinContent(i));
	if "MHT2" in parse[3]:
		MHTTTbar.Fill(525, LL.GetBinContent(i))
		MHTSignal.Fill(525, SignalT2tt.GetBinContent(i));
	if "MHT3" in parse[3]:
		MHTTTbar.Fill(900, LL.GetBinContent(i))
		MHTSignal.Fill(900, SignalT2tt.GetBinContent(i));
	if "HT0" in parse[4] or "HT3" in parse[4] :
                HTTTbar.Fill(350, LL.GetBinContent(i))
                HTSignal.Fill(350, SignalT2tt.GetBinContent(i));
	if "HT1" in parse[4] or "HT4" in parse[4] or "HT6" in parse[4] or "HT8" in parse[4] :
                HTTTbar.Fill(750, LL.GetBinContent(i))
                HTSignal.Fill(750, SignalT2tt.GetBinContent(i));
	if "HT9" in parse[4] or "HT7" in parse[4] or "HT5" in parse[4] or "HT2" in parse[4] :
                HTTTbar.Fill(1250, LL.GetBinContent(i))
                HTSignal.Fill(1250, SignalT2tt.GetBinContent(i));

fout=TFile("Projections1D.root", "RECREATE");
BTagsSignal.Write("BTags1DProjT2tt")	
BTagsTTbar.Write("BTags1DProjTTBar")
NJetsSignal.Write("NJets1DProjT2tt")	
NJetsTTbar.Write("NJets1DProjTTBar")
HTSignal.Write("HT1DProjT2tt")	
HTTTbar.Write("HT1DProjTTBar")
MHTSignal.Write("MHT1DProjT2tt")	
MHTTTbar.Write("MHT1DProjTTBar")
fout.Close()	

